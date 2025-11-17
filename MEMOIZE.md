# Project Memoization

This file contains important decisions and patterns to remember throughout the project lifecycle.

---

## Prompt Logging Protocol

**Decision**: All prompts to Claude Code MUST be appended to PROMPTS.md

**Rationale**: Maintain complete context history for project development, enable traceability of decisions, and provide documentation for future reference.

**Implementation**: When receiving a new prompt, append it to PROMPTS.md with:
- Date
- Prompt number
- Full prompt text
- Context/tags for categorization

---

## Port Configuration

**Decision**: Web application runs on port 7676 ONLY

**Source**: CLAUDE.md project instructions

---

## Architecture Decisions

**Decision**: Agent-native RAG architecture with zero-cost, locally-running services

**Key Technologies**:
- ChromaDB + DuckDB (vector database)
- Ollama (local LLM)
- Redis Streams (event processing)
- MCP (Model Context Protocol)
- JSON-LD (data schema and ontology)

**Source**: X-UAS-CONTEXT-ENGINEERING-PROMPT.md

---

## Project Focus

**Decision**: UAV comparison web application focusing on visualization of platforms, capabilities, missions, sensors, payloads, costs, RF spectrum, and proliferation data

**Key Features**:
- Graph database and visualization
- JSON-LD ontology
- Ollama-based agentic LLM interface
- MCP tools for database queries, interactive elements, charts, and alerts
- Focus on UAVs in research, development, and early production stages

**Primary Sources**:
- The War Zone (www.twz.com) for cutting-edge UAV journalism
- Wikipedia UAV articles
- JAPCC C-UAS documentation
- Government procurement documentation (US DoD, China, Ukraine, Russia, Israel, Iran, NATO)

---
