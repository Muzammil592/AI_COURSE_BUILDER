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
* **Deterministic Schema Generation:** Transitioned from mock data to actual model evaluation by integrating the `google-genai` SDK. Programmed the system to feed dynamic prompt inputs into the generative model layers.
* **Zero-Variance System Structuring:** Configured a strict low-temperature constraint ($T = 0.3$) and locked the response mime-type to `application/json`, forcing the AI model to fit its response directly into our nested data layout:
  $$\text{CourseStructureResponse} \longrightarrow \text{ModuleItem} \longrightarrow \text{LessonItem} \longrightarrow \text{QuizItem}$$

### Data Fetching Asynchronous
* **Concurrent Video Ingestion:** Engineered an asynchronous web worker leveraging the YouTube Data API (`google-api-python-client`) to extract targeted educational videos. 
* **Non-blocking Event Loop Optimization:** Implemented parallel execution using `asyncio.gather()`. Instead of querying YouTube links linearly (which drops network speeds), the system triggers all queries concurrently, mapping out URLs over background execution slots without stalling main HTTP traffic.

### Compilation Issues & Dockerization Error Resolved
* **Registry Dependency Patching:** Diagnosed and corrected a critical build blocker caused by deprecated PyPI SDK pointers, successfully shifting image build configurations onto the active `google-genai==2.10.0` specification tracking array.
* **Fault-Tolerant API Fallbacks:** Written a graceful dev-mode intercept inside the scraping module to capture missing or depleted environment api keys, maintaining continuous runtime pipeline operation even during quota limits.

---

## Day 3: Node.js Data Orchestration, Spec Modernization & State Persistence

### Relational Schema Blueprinting
* **Hybrid Document Modeling:** Engineered a granular Mongoose schema layout in the Node.js layer parsing directly from strict Pydantic outputs, structurally caching modules, lesson entities, and metadata blocks seamlessly.
* **Transactional Query Optimization:** Affixed high-performance field indices over prompt attributes ensuring blazing-fast read lookups.

### Cross-Container Ingress & Pipeline Resilience
* **Internal Routing Channels:** Linked Express processing routers down into the hidden private bridge layer, abstracting connection pipelines using native container host targets (`http://AISERVICE:8000`).
* **Regex Protection Layer:** Patched a critical validation crash by implementing an absolute character-escaping array on cache search checks, preventing special-character prompts (e.g., `"C++"`) from disrupting regular expression evaluation loops.
* **Specification Modernization:** Removed the deprecated root `version` tag from `docker-compose.yml` to satisfy modern Compose Engine parsing guidelines and completely eliminate console warning overhead.

### Model Optimization & Global Insulation Fail-Safe
* **Token Ingestion Optimization:** Shifted core execution targeting from `gemini-2.5-pro` to the faster, high-quota `gemini-2.5-flash` model within `main.py` to leverage enhanced throughput bounds and reduce latency on structured JSON builds.
* **Global Insulation Fail-Safe Interceptor:** Integrated a rigorous exception-catching interceptor in the `AISERVICE` layer. In the event of a `429 RESOURCE_EXHAUSTED` trigger or external quota depletion, the microservice immediately hot-swaps to an internally built, dynamically mapped fallback blueprint payload. This ensures the Day 3 end-to-end database pipeline never halts.

### Outcome
The full data orchestration layer is successfully unified and hardened. User queries cleanly cycle through a robust regex validation intercept, resolve via an ultra-fast, high-quota model pipeline (or an automated data insulation fallback), and securely commit states directly into the persistent storage engine with transparent cache indicators. Ready for Day 4 frontend dashboard interface canvas construction.
