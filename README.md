# Enterprise AI TPM Agent: Context-Aware Jira Automation Pipeline

An enterprise-grade Retrieval-Augmented Generation (RAG) pipeline designed to automate the creation of complex, multi-platform Jira Epics. By leveraging local vector storage and strict LLM guardrails, this tool enforces engineering standards, eliminates context bleed, and features a continuous-learning feedback loop.

## 📈 Business Value & Impact
Traditional AI text generators fail in enterprise environments because they lack operational context and hallucinate generic agile workflows. This system was built with strict **Technical Program Management (TPM)** principles to solve actual engineering bottlenecks:
* **Zero-Hallucination Architecture:** Grounded strictly in historical Jira tickets. If the engineering team hasn't done it before, the AI won't invent it.
* **Deterministic Compliance:** Enforces 100% compliance with internal definition-of-done standards (e.g., automatically appending mandatory QA, TestFlight, and Release steps to all mobile tickets).
* **Cross-Discipline Orchestration:** Autonomously maps out complex workflows across Design, Backend, iOS, and Android teams in the correct operational sequence.
* **Reduced Planning Overhead:** Turns a 1-hour Epic breakdown process into a 15-second human-in-the-loop approval workflow.

## 🧠 System Architecture

The pipeline moves away from basic "wrapper" AI and utilizes an **Advanced RAG (Retrieval-Augmented Generation)** architecture with smart routing and a self-healing memory loop.

### 1. Smart Ingestion & Metadata Routing
Historical Jira tickets are ingested, chopped using LangChain text splitters, and embedded using `gemini-embedding-001`. Crucially, a custom metadata engine extracts the **Platform** (iOS, Android, Backend) and **Tenant/App ID** (Tricode) before saving to a local **ChromaDB** vector database. 

### 2. Context Isolation (Preventing Context Bleed)
When a user requests a new feature, the system queries the vector database and groups historical examples strictly by Platform. This prevents the LLM from accidentally applying Backend API logic to an iOS UI task.

### 3. Enforced Generation (The "Golden Example")
The retrieved context is passed to `gemini-2.5-flash` alongside:
* **Pydantic Schemas:** Forcing strict JSON output formatted exactly for the Jira API.
* **Dynamic Protocol Guidelines:** Soft-prompting the AI with complex workflows (e.g., "App Update Protocol") while allowing it to adapt to user exceptions.
* **Hardcoded Checklists:** Appending mandatory release pipeline subtasks regardless of LLM probability.

### 4. The Self-Healing UI Feedback Loop
Built on **Streamlit**, the frontend acts as a human-in-the-loop approval station. If the TPM edits the AI-generated draft before pushing it to Jira, the system triggers a `save_to_memory` function, embedding the perfected JSON back into ChromaDB as a "Human Approved Gold Standard." The system permanently learns from its mistakes without requiring model fine-tuning.

## 🛠️ Tech Stack
* **LLM Engine:** Google Gemini (`gemini-2.5-flash` for generation, `gemini-embedding-001` for vectors)
* **Vector Database:** ChromaDB (Local SQLite/Parquet storage for enterprise privacy)
* **Backend Logic:** Python, LangChain (RecursiveCharacterTextSplitter), Pydantic (Schema validation)
* **Frontend UI:** Streamlit
* **Integrations:** Jira Cloud REST API

## 🚀 Local Setup & Installation

**1. Clone the repository and setup virtual environment**
```bash
git clone [https://github.com/yourusername/sprint-forecaster-ai.git](https://github.com/yourusername/sprint-forecaster-ai.git)
cd sprint-forecaster-ai
python3 -m venv venv
source venv/bin/activatego