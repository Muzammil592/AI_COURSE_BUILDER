# AI Course Builder - Microservices Engineering Log

## Day 1: Project Setup and Components Layers Establishment

### Infrastructure Foundation
* **Unified Monorepo Architecture:** Established a decoupled multi-tier monorepo structure with synchronized directory mappings (`/Backend`, `/AISERVICE`) to optimize development workflows and microservice orchestration.

### AI Service Initialization (AISERVICE)
* **Production-Grade FastAPI Scaffolding:** Configured an asynchronous Python 3.10 microservice baseline engineered for high-throughput AI inference and data formatting workloads.
* **Strict Runtime Contract Enforcement:** Implemented strict structural response schemas utilizing nested **Pydantic v2** validation matrices to eliminate structural corruption and enforce deterministic JSON compliance on raw upstream outputs.

### Backend Orchestration Layer (Backend)
* **Decoupled Gateway Routing:** Initialized an event-driven Node.js and Express gateway leveraging modern ECMAScript Modules (`"type": "module"`) for optimal application layer performance.

### Containerization & Service Networking
* **Multi-Container Orchestration:** Engine configuration driven by modern Docker Compose specifications to systematically compile and manage three core decoupled layers: Persistent Storage (`mongodb:latest`), Business Logic (`Backend`), and AI Worker Core (`AISERVICE`).
* **Isolated Virtual Bridge Network:** Implemented a secure private network driver (`course_builder_network`), forcing internal communication loops to resolve securely over native container DNS names (`http://AISERVICE:8000`).

---

## Day 2: AI Core Inference & Media Hydration Pipeline

### Structured LLM Synthesis
* **Deterministic Schema Generation:** Transitioned from mock data to actual model evaluation by integrating the `google-genai` SDK (`v2.10.0`). Programmed the system to feed dynamic prompt inputs into the `gemini-2.5-pro` model.
* **Zero-Variance System Structuring:** Configured a strict low-temperature constraint ($T = 0.3$) and locked the response mime-type to `application/json`, forcing the AI model to fit its response directly into our nested data layout:
  $$\text{CourseStructureResponse} \longrightarrow \text{ModuleItem} \longrightarrow \text{LessonItem} \longrightarrow \text{QuizItem}$$

### Data Fetching Asynchronous
* **Concurrent Video Ingestion:** Engineered an asynchronous web worker leveraging the YouTube Data API (`google-api-python-client`) to extract targeted educational videos. 
* **Non-blocking Event Loop Optimization:** Implemented parallel execution using `asyncio.gather()`. Instead of querying YouTube links linearly (which drops network speeds), the system triggers all queries concurrently, mapping out URLs over background execution slots without stalling main HTTP traffic.

### Compilation Issues & Dockerization Error Resolved
* **Registry Dependency Patching:** Diagnosed and corrected a critical build blocker caused by deprecated PyPI SDK pointers, successfully shifting image build configurations onto the active `google-genai==2.10.0` specification tracking array.
* **Fault-Tolerant API Fallbacks:** Written a graceful dev-mode intercept inside the scraping module to capture missing or depleted environment api keys, maintaining continuous runtime pipeline operation even during quota limits.

### Outcome
The `AISERVICE` runtime layer is now capable of parsing unformatted raw prompts, generating mathematically validated course documents, and auto-hydrating them with live streaming URLs concurrently. Ready for Day 3 state-persistence and orchestrator bridge loops.
