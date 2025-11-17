# Project Prompts Log

This file documents all prompts entered into the X-UAV project for reference and context tracking.

---

## 2025-11-16

### Prompt 1: Initial Project Definition and Research Request

**Date**: 2025-11-16

**Prompt**:
First, create a PROMPTS.md file that documents every prompt entered into this project. Memoize this decision, all prompts to Claude Code get appended to PROMPTS.md. This project is a web application for the purpose of comparisons between different unmanned aerial vehicles. This will focus on the visualization of platforms, capabilities, missions, sensor and other payloads, costs, RF spectrum used, proliferation, and other highly contextual information about UAVs. Go into research mode. Search this primary sources and all of their cited references: https://en.wikipedia.org/wiki/Unmanned_aerial_vehicle, https://www.japcc.org/chapters/c-uas-introduction/, https://en.wikipedia.org/wiki/Unmanned_combat_aerial_vehicle Formulate a plan for developing this web application, to allow comparison between different UAVs. Conduct research for how federal governments have decided on the missions, capabilities, and procurements of UAV platforms. Focus specifically on the United States Department of Defense/Department of War procurement, but also China, Ukraine, Russia, Israel, and Iran. Research countries currently expanding their UAV capabilities, particularly NATO countries, and document the published decision criteria that they have indicated will be used. This project must document existing UAVs but critically will focus on UAVs in research, development, and early production stages. Leverage www.twz.com as the primarly source for journalist articles describing cutting edge capabilities in UAVs. Plan to include a graph database and graph based visualization where a user can see and crawl the network of common data such as UAV type, mission, manufacturing country, procurement country, sensors, weapons, named military units, and other data well characterized by a graph knowledge base. Include in this plan an ontology for classifying all data. Plan on using a Javascript Object Notaion for Linked Data (JSON-LD) schema for sharing data types and providing context and for structring data within the graph, ontology, html, and web services. Plan on a locally hosted ollama based agentic LLM interface for interacting with the web application. Plan on providing MCP tools to the chat agent. Example MCP tools should include: ability to search the database for UAVs with capabilities that match a user prompt; ability to provide interactive html elements to corresponds to UAVs or other data available within the application; ability to create charts depicting the performance envelope of UAVs in a user prompt; ability to create alerts based on user prompt, which monitor selected media for references to UAVs of interest. Research the web for websites providing comparisons in different contexts. Include consumer technology, physical hardware, and video game websites such as: https://worldofwarplanes.com/warplanes/compare/, https://worldofwarplanes.com/warplanes/, https://shiptool.st/, https://www.apple.com, https://boltdepot.com/, https://cmano-db.com/aircraft/1580/, cmano-db.com/compare.php, https://www.edmunds.com/car-comparisons/?veh1=402075530|hatchback&veh2=402084038|hatchback&veh3=402086618|suv&veh4=402070372|suv, https://fleetyards.net/compare/ships/?models%5B%5D=325a&models%5B%5D=350r Research the web for other tools focused on the visual design of web applications and comparison tool. Prepare a detailed plan for this project that we will later review using Claude Code. Suggest areas for improvement to the plan.

**Context**: Initial project setup for UAV comparison web application with graph database, JSON-LD schema, Ollama integration, and MCP tools.

---

### Prompt 2: CCA Research and Mission Set Emphasis

**Date**: 2025-11-16

**Prompt**:
Search the web for information on the Cooperative Combat Aircraft, focusing on the systems in development by Anduril, General Atomics Aeronautical, and competitors by Lockheed Martin, Boeing, ShieldAI, and Helsing Defence. Then update this project plan to emphasize UAV mission sets, comparisons, displays of data, and alternatives not just between the different company offers, but between different variants or possible capabilities for each company's main platform.

**Context**: Refining project plan to emphasize mission-set based comparisons and variant/capability-level analysis for CCA programs. Focus on company platforms and their multiple configuration options.

---

### Prompt 3: Implementation of PROJECT-PLAN.md

**Date**: 2025-11-16

**Prompt**:
Implement the @PROJECT-PLAN.md

**Context**: Beginning implementation of Phase 1 (Foundation) from the comprehensive 24-week project plan. Setting up Docker environment, FastAPI backend, Vue.js frontend, and database connections.

---
