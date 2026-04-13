import os
import re
import json
import uuid
import chromadb
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# 1. Open the Safe
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# 2. THE BLUEPRINT (Pydantic Schema)
class Subtask(BaseModel):
    summary: str = Field(
        description="Short, actionable title of the subtask matching the Tricode naming convention."
    )
    description: str = Field(
        description="Detailed technical requirement based strictly on historical context."
    )


class Story(BaseModel):
    summary: str = Field(
        description="User story title matching the Tricode naming convention."
    )
    description: str = Field(
        description="Standard agile format: As a [user], I want [action] so that [value]"
    )
    subtasks: list[Subtask] = Field(description="List of required technical subtasks")


class EpicProposal(BaseModel):
    epic_summary: str = Field(
        description="High level initiative title matching the Tricode naming convention."
    )
    epic_description: str = Field(description="Business value and goals")
    stories: list[Story] = Field(description="List of stories under this epic")


# 3. Our Vector Translation Tool (Embedding Function)
class GeminiEmbeddingFunction(chromadb.EmbeddingFunction):
    def __init__(self):
        super().__init__()

    def __call__(self, input: chromadb.Documents) -> chromadb.Embeddings:
        embeddings = []
        for text in input:
            response = client.models.embed_content(
                model="gemini-embedding-001", contents=text
            )
            embeddings.append(response.embeddings[0].values)
        return embeddings


def run_agent(user_prompt: str):
    # --- NEW: Dynamic Tricode Parsing ---
    tricode_match = re.search(r"App Tricode:\s*([A-Z0-9]+)", user_prompt)
    active_tricode = tricode_match.group(1) if tricode_match else "TRICODE"

    # 4. Connect to your local memory bank
    db_dir = Path(__file__).parent.parent / "data" / "chroma_db"
    chroma_client = chromadb.PersistentClient(path=str(db_dir))

    collection = chroma_client.get_collection(
        name="jira_memory", embedding_function=GeminiEmbeddingFunction()
    )

    # 5. RETRIEVAL (The 'R' in RAG)
    print("Searching memory for historical Jira context...")
    results = collection.query(
        query_texts=[user_prompt],
        n_results=20,  # Cast a wide net across ALL apps
    )

    # --- NEW: Smart Platform Grouping ---
    platform_groups = {
        "iOS": [],
        "Android": [],
        "Backend": [],
        "QA": [],
        "Design": [],
        "Web": [],
        "Other": [],
    }

    if results["documents"] and results["metadatas"]:
        for i, doc in enumerate(results["documents"][0]):
            meta = results["metadatas"][0][i]
            raw_platform = meta.get("platform", "Other")

            plat_lower = raw_platform.lower()
            if "ios" in plat_lower:
                plat_key = "iOS"
            elif "android" in plat_lower:
                plat_key = "Android"
            elif "backend" in plat_lower or "api" in plat_lower:
                plat_key = "Backend"
            elif "qa" in plat_lower:
                plat_key = "QA"
            elif "design" in plat_lower:
                plat_key = "Design"
            elif "web" in plat_lower in plat_lower:
                plat_key = "Web"
            else:
                plat_key = "Other"

            platform_groups[plat_key].append(doc)

    historical_context = ""
    for plat, docs in platform_groups.items():
        if docs:
            historical_context += (
                f"\n### === {plat.upper()} HISTORICAL EXAMPLES === ###\n"
            )
            for idx, d in enumerate(docs):
                historical_context += f"--- Example {idx + 1} ---\n{d}\n\n"

    # 6. THE PERSONA & FEW-SHOT PROMPT (Strict Guardrails)
    print("Thinking and drafting project proposal...")
    system_instructions = f"""
    You are an expert Technical Program Manager at YinzCam. Your core responsibility is translating high-level feature requests into highly detailed, technically accurate Jira Epics, Stories, and Subtasks.

    CRITICAL INSTRUCTIONS & GUARDRAILS:
    1. STRICT MIMICRY: You MUST mimic the exact technical terminology, architecture, and subtask breakdown found in the [HISTORICAL EXAMPLES]. 
    2. ZERO GENERIC AGILE: Do NOT invent generic or boilerplate Agile steps (e.g., do not write "Gather requirements", "Write unit tests", or "Deploy to staging" unless it specifically matches the pattern in our historical data).
    3. NO HALLUCINATIONS: Rely EXCLUSIVELY on the provided history to inform the technical architecture.
    4. MANDATORY NAMING CONVENTION: Every single ticket, story, and subtask you generate MUST follow this exact format: [Tricode]: [Platform]: [Work Description]
       - Valid Platforms: Backend, iOS, Android, QA, Design, AM, PM, Client, Web.

    MANDATORY PLATFORM CHECKLISTS (DEFINITION OF DONE):
    Depending on the platform of the story being generated, you MUST automatically append the following subtasks, completely verbatim:

    If the Story involves the iOS platform:
    - "{active_tricode}: iOS: Merge master"
    - "{active_tricode}: iOS: Generate TF + QA build"
    - "{active_tricode}: QA: Full QA"
    - "{active_tricode}: iOS: SUBMIT"
    - "{active_tricode}: iOS: RELEASE"
    - "{active_tricode}: iOS: Reintegrate"

    If the Story involves the Android platform:
    - "{active_tricode}: Android: Merge master"
    - "{active_tricode}: Android: Generate QA build"
    - "{active_tricode}: QA: Full QA"
    - "{active_tricode}: Android: SUBMIT"
    - "{active_tricode}: Android: RELEASE"

    *** APP UPDATE REFERENCE GUIDELINE ***
    If the user's request involves a routine "App Update", SDK update, or season refresh, use the following JSON structure as your BASELINE GUIDELINE. 
    You do NOT need to copy these exact tasks verbatim if the user specifies different requirements (e.g., a different SDK version, or skipping design tasks). However, you should strongly mimic this cross-discipline operational flow (Design handoff -> Dev -> QA -> Submit -> Release). Adapt the specific subtasks dynamically based on the [USER REQUEST] and [HISTORICAL CONTEXT]:
    
    {{
        "epic_summary": "{active_tricode}: App Update",
        "epic_description": "Routine app update including SDK upgrades, design asset refreshes, and standard release pipelines.",
        "stories": [
            {{
                "summary": "{active_tricode}: iOS: App Update",
                "description": "Update the iOS app with the latest SDKs, design assets, and prepare for App Store release.",
                "subtasks": [
                    {{"summary": "{active_tricode}: iOS: Update TM SDK to v3.15", "description": "Update Ticketmaster SDK to version 3.15."}},
                    {{"summary": "{active_tricode}: iOS: Add support to Age Gate", "description": "Implement Age Gate functionality for iOS."}},
                    {{"summary": "{active_tricode}: Design: Update first stage splash screen", "description": "Upload the updated first stage splash screen assets in iOS design repo."}},
                    {{"summary": "{active_tricode}: iOS: Update primary and secondary colors", "description": "Update colors in the iOS design sheet."}},
                    {{"summary": "{active_tricode}: iOS: Merge Master", "description": "Merge master branch into release branch."}}
                ]
            }},
            {{
                "summary": "{active_tricode}: Android: App Update",
                "description": "Update the Android app with the latest SDKs, design assets, and prepare for Play Store release.",
                "subtasks": [
                    {{"summary": "{active_tricode}: Android: Update TM SDK to v3.15", "description": "Update Ticketmaster SDK to version 3.15."}},
                    {{"summary": "{active_tricode}: Android: Update primary and secondary colors", "description": "Update colors in the Android design sheet."}},
                    {{"summary": "{active_tricode}: Android: Merge Master", "description": "Merge master branch into release branch."}}
                ]
            }}
        ]
    }}

    HISTORICAL CONTEXT (Organized by Platform to avoid context bleed):
    {historical_context}
    """

    # 7. GENERATION (The 'G' in RAG)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[system_instructions, f"USER REQUEST:\n{user_prompt}"],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=EpicProposal,
            temperature=0.1,
        ),
    )

    return response.text


# --- NEW: UI Feedback Loop Database Push ---
def save_to_memory(approved_plan: dict, tricode: str):
    """Saves human-approved JSON plans back into the vector database."""
    db_dir = Path(__file__).parent.parent / "data" / "chroma_db"
    chroma_client = chromadb.PersistentClient(path=str(db_dir))
    collection = chroma_client.get_collection(
        name="jira_memory", embedding_function=GeminiEmbeddingFunction()
    )

    # Convert the perfected JSON into a searchable string
    doc_text = f"HUMAN APPROVED GOLD STANDARD:\n{json.dumps(approved_plan, indent=2)}"

    # Save it to the database with a special metadata tag
    collection.add(
        documents=[doc_text],
        metadatas=[{"tricode": tricode, "type": "human_approved", "platform": "mixed"}],
        ids=[f"approved_{uuid.uuid4()}"],
    )
    print(f"🧠 AI Memory updated with new human-approved plan for {tricode}.")


if __name__ == "__main__":
    print("\n🤖 Virtual TPM Initialized.\n")

    # This is our test prompt.
    test_request = "App Tricode: NFLPIT\n\nFeature Request: We need to build a new automated email notification system that alerts users when their password is changed."

    print(f"User Request: {test_request}\n")
    final_json = run_agent(test_request)
    print("\n✅ GENERATED JIRA PLAN (JSON):")
    print(final_json)
