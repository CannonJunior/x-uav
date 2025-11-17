# X-UAV Ontology Documentation

## Overview

The X-UAV ontology is a semantic knowledge graph for representing Collaborative Combat Aircraft (CCA) platforms, their variants, mission configurations, and relationships to manufacturers, programs, and technologies.

**Version**: 1.0
**Last Updated**: 2025-11-16
**Database**: ArangoDB Graph Database
**Semantic Format**: JSON-LD 1.1

---

## Table of Contents

1. [Ontology Structure](#ontology-structure)
2. [Entity Types (Vertex Collections)](#entity-types-vertex-collections)
3. [Relationship Types (Edge Collections)](#relationship-types-edge-collections)
4. [JSON-LD Context](#json-ld-context)
5. [Graph Traversal Patterns](#graph-traversal-patterns)
6. [Example Queries](#example-queries)
7. [Data Model Design Principles](#data-model-design-principles)

---

## Ontology Structure

The X-UAV ontology follows a hierarchical structure representing the progression from high-level platform families down to specific mission configurations:

```
Program
   ↓
Platform Family → Manufacturer
   ↓                    ↓
Platform Variant ← Autonomy Provider
   ↓
Mission Configuration
   ↓
Mission Type
```

### Namespace Definitions

The ontology uses the following namespace prefixes (defined in `context.jsonld:1-11`):

- `@vocab`: `https://x-uav.local/ontology#` (default namespace)
- `schema`: `https://schema.org/`
- `mil`: `https://x-uav.local/military#`
- `uav`: `https://x-uav.local/uav#`
- `geo`: `https://x-uav.local/geography#`
- `spec`: `https://x-uav.local/specification#`

---

## Entity Types (Vertex Collections)

### 1. Countries (`countries`)

Represents nations involved in UAV development or operation.

**Type**: `geo:Country`

**Properties**:
- `_key` (string): ISO country code (lowercase, e.g., "us", "au")
- `name` (string): Full country name
- `iso_code` (string): ISO 3166-1 alpha-2 code
- `region` (string): Geographic region
- `nato_member` (boolean): NATO membership status

**Example**:
```json
{
  "_key": "us",
  "name": "United States",
  "iso_code": "US",
  "region": "North America",
  "nato_member": true
}
```

---

### 2. Manufacturers (`manufacturers`)

Defense contractors and technology companies developing UAV platforms.

**Type**: `schema:Organization`

**Properties**:
- `_key` (string): Kebab-case identifier
- `name` (string): Official company name
- `headquarters` (string): Location of headquarters
- `country` (string): Country of origin
- `type` (string): Company classification

**Example**:
```json
{
  "_key": "anduril",
  "name": "Anduril Industries",
  "headquarters": "Costa Mesa, California",
  "country": "United States",
  "type": "Private defense technology company"
}
```

---

### 3. Programs (`programs`)

Military acquisition programs funding CCA development.

**Type**: `mil:Program`

**Properties**:
- `_key` (string): Program identifier
- `name` (string): Official program name
- `country` (string): Sponsoring nation
- `budget` (number): Total budget in USD
- `start_date` (string): ISO 8601 date
- `status` (string): Current status (e.g., "Development", "Production")

**Example**:
```json
{
  "_key": "cca-increment-1",
  "name": "CCA Increment 1",
  "country": "United States",
  "budget": 6000000000,
  "start_date": "2024-04-24",
  "status": "Development"
}
```

---

### 4. Missions (`missions`)

Mission types that CCAs can perform.

**Type**: `mil:Mission`

**Properties**:
- `_key` (string): Mission type identifier
- `name` (string): Mission name
- `category` (string): Mission category
- `description` (string): Detailed mission description

**Example**:
```json
{
  "_key": "isr",
  "name": "ISR",
  "category": "Intelligence, Surveillance, Reconnaissance",
  "description": "Gathering and processing information about adversaries and the operational environment"
}
```

**Supported Mission Types**:
- `isr`: Intelligence, Surveillance, Reconnaissance
- `strike`: Offensive Air Operations
- `electronic-warfare`: EW operations
- `decoy`: Defensive Operations
- `air-to-air`: Air Superiority

---

### 5. Platform Families (`platform_families`)

High-level UAV platform families representing design lineages.

**Type**: `uav:PlatformFamily`

**Properties**:
- `_key` (string): Family identifier
- `name` (string): Platform family name
- `manufacturer` (string): Primary manufacturer
- `program` (string): Associated program
- `base_technology` (string): Core technologies
- `description` (string): Platform description
- `country` (string): Country of origin

**Example**:
```json
{
  "_key": "fury",
  "name": "Fury",
  "manufacturer": "Anduril Industries",
  "program": "CCA Increment 1",
  "base_technology": "Lattice OS, MOSA architecture",
  "description": "High-performance, multi-mission Group 5 autonomous air vehicle",
  "country": "United States"
}
```

---

### 6. Platform Variants (`platform_variants`)

Specific airframe variants within a platform family.

**Type**: `uav:PlatformVariant`

**Properties**:
- `_key` (string): Variant identifier
- `name` (string): Full variant name
- `designation` (string): Military designation (e.g., "YFQ-44A")
- `airframe_type` (string): Airframe configuration
- `development_status` (string): Current development phase
- `first_flight` (string|null): ISO 8601 date or null
- `description` (string): Variant description

**Example**:
```json
{
  "_key": "yfq-44a",
  "name": "YFQ-44A Fury",
  "designation": "YFQ-44A",
  "airframe_type": "Fixed-wing",
  "development_status": "Flight testing",
  "first_flight": "2025-10-31",
  "description": "Anduril's Increment 1 CCA prototype with Shield AI Hivemind autonomy"
}
```

---

### 7. Mission Configurations (`mission_configurations`)

Specific payload and mission configurations for platform variants.

**Type**: `uav:MissionConfiguration`

**Properties**:
- `_key` (string): Configuration identifier
- `name` (string): Configuration name
- `mission_type` (string): Primary mission type
- `payload_description` (string): Payload details
- `estimated_cost_per_sortie` (number): Cost in USD

**Example**:
```json
{
  "_key": "fury-isr",
  "name": "Fury-ISR",
  "mission_type": "ISR",
  "payload_description": "EO/IR sensor package, SAR/GMTI radar, extended loiter optimization",
  "estimated_cost_per_sortie": 45000
}
```

---

### 8. Technologies (`technologies`)

Enabling technologies used in UAV platforms.

**Type**: `uav:Technology`

**Properties**:
- `_key` (string): Technology identifier
- `name` (string): Technology name
- `type` (string): Technology category
- `maturity_level` (string): Development maturity
- `description` (string): Technology description

**Example**:
```json
{
  "_key": "hivemind-ai",
  "name": "Hivemind AI",
  "type": "Autonomy Software",
  "maturity_level": "Operational",
  "description": "Shield AI's autonomous pilot for GPS-denied environments"
}
```

---

## Relationship Types (Edge Collections)

### 1. `manufactured_by`

Links platform families to their manufacturers.

**From**: `platform_families`
**To**: `manufacturers`

**Example**: `fury → anduril`

---

### 2. `developed_under`

Links platform families to their development programs.

**From**: `platform_families`
**To**: `programs`

**Example**: `fury → cca-increment-1`

---

### 3. `belongs_to_family`

Links platform variants to their parent families.

**From**: `platform_variants`
**To**: `platform_families`

**Example**: `yfq-44a → fury`

---

### 4. `configured_from`

Links mission configurations to platform variants.

**From**: `mission_configurations`
**To**: `platform_variants`

**Example**: `fury-isr → yfq-44a`

---

### 5. `configured_for`

Links mission configurations to mission types.

**From**: `mission_configurations`
**To**: `missions`

**Example**: `fury-isr → isr`

---

### 6. `provides_autonomy`

Links technology providers to platform variants they supply autonomy software for.

**From**: `manufacturers`
**To**: `platform_variants`

**Example**: `shield-ai → yfq-44a`

---

### 7. `implements_tech`

Links platform variants to technologies they implement.

**From**: `platform_variants`
**To**: `technologies`

**Example**: `yfq-44a → hivemind-ai`

---

## JSON-LD Context

The ontology uses JSON-LD 1.1 for semantic interoperability. The context file (`context.jsonld`) defines:

1. **Type mappings** (lines 12-23): Map entity types to semantic URIs
2. **Property mappings** (lines 25-171): Map properties to schema.org and custom vocabularies
3. **Type coercion** (lines 28-50, 56-100): Enforce proper data types for URIs, dates, and measurements
4. **Container definitions** (lines 114-140): Define set-based relationships

**Key Features**:
- Uses `@type: "@id"` for relationship properties to ensure proper linking
- Uses `schema:QuantitativeValue` for physical specifications
- Uses `schema:PriceSpecification` for costs
- Uses `schema:Date` for temporal data

---

## Graph Traversal Patterns

### Pattern 1: Platform Lineage

**Query**: Find all configurations for a given platform family

```
platform_families/{family}
  → belongs_to_family (inbound)
  → platform_variants
  → configured_from (inbound)
  → mission_configurations
```

**Example**: Fury family configurations

---

### Pattern 2: Technology Stack

**Query**: Find all technologies used by a platform variant

```
platform_variants/{variant}
  → implements_tech (outbound)
  → technologies
```

**Example**: YFQ-44A technology stack (Lattice OS, Hivemind AI, MOSA)

---

### Pattern 3: Supply Chain

**Query**: Trace a platform's manufacturers and autonomy providers

```
platform_variants/{variant}
  → belongs_to_family (outbound)
  → platform_families
  → manufactured_by (outbound)
  → manufacturers

platform_variants/{variant}
  → provides_autonomy (inbound)
  → manufacturers
```

---

### Pattern 4: Mission Capabilities

**Query**: Find all platform configurations capable of a specific mission

```
missions/{mission}
  → configured_for (inbound)
  → mission_configurations
  → configured_from (outbound)
  → platform_variants
```

**Example**: All ISR-capable platforms

---

## Example Queries

### AQL Query 1: Find All Fury Configurations

```aql
FOR family IN platform_families
  FILTER family._key == 'fury'
  FOR variant IN 1..1 INBOUND family belongs_to_family
    FOR config IN 1..1 INBOUND variant configured_from
      RETURN {
        variant: variant.name,
        configuration: config.name,
        mission: config.mission_type,
        cost: config.estimated_cost_per_sortie
      }
```

---

### AQL Query 2: Technology Providers for CCA Increment 1

```aql
FOR program IN programs
  FILTER program._key == 'cca-increment-1'
  FOR family IN 1..1 INBOUND program developed_under
    FOR variant IN 1..1 INBOUND family belongs_to_family
      FOR tech IN 1..1 OUTBOUND variant implements_tech
        RETURN DISTINCT {
          platform: variant.name,
          technology: tech.name,
          type: tech.type
        }
```

---

### AQL Query 3: Full Provenance Chain

```aql
FOR config IN mission_configurations
  FILTER config._key == 'fury-isr'
  FOR variant IN 1..1 OUTBOUND config configured_from
    FOR family IN 1..1 OUTBOUND variant belongs_to_family
      FOR mfr IN 1..1 OUTBOUND family manufactured_by
        FOR program IN 1..1 OUTBOUND family developed_under
          RETURN {
            configuration: config.name,
            variant: variant.designation,
            family: family.name,
            manufacturer: mfr.name,
            program: program.name,
            budget: program.budget
          }
```

---

## Data Model Design Principles

### 1. **Separation of Concerns**

- **Platform families** represent design lineages
- **Platform variants** represent specific airframes
- **Mission configurations** represent operational setups

This allows the same variant to have multiple configurations without data duplication.

---

### 2. **Bidirectional Relationships**

All relationships are explicitly modeled as edges, enabling:
- Forward traversal: Family → Variants → Configurations
- Reverse traversal: Configuration → Variant → Family
- Multi-hop queries across the entire graph

---

### 3. **Semantic Web Compatibility**

JSON-LD context enables:
- Export to RDF/OWL formats
- Integration with external ontologies (schema.org, military ontologies)
- SPARQL query compatibility (via ArangoDB RDF adapter)

---

### 4. **Extensibility**

The schema supports future additions:
- New edge types (e.g., `competes_with`, `derived_from`)
- Additional vertex collections (e.g., `sensors`, `weapons`, `operators`)
- External data linking via `sameAs` property

---

### 5. **Cost Tracking**

Cost data is embedded at the configuration level (`estimated_cost_per_sortie`) rather than variant level, as costs vary significantly based on payload and mission profile.

---

## References

- **JSON-LD Specification**: https://www.w3.org/TR/json-ld11/
- **Schema.org**: https://schema.org/
- **ArangoDB Graph Docs**: https://www.arangodb.com/docs/stable/graphs.html
- **CCA Program Overview**: USAF CCA Increment 1 (2024)

---

**Maintained by**: X-UAV Project Team
**Contact**: See `README.md` for contribution guidelines
