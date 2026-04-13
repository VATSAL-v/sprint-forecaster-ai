import os
from dotenv import load_dotenv
from atlassian import Jira
from google import genai

# This forces Python to look in the main folder for the .env file
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

print("Testing connections... Please wait a moment.\n")

# ---------------------------------------------------------
# SAFETY CHECK: Did the .env file load?
# ---------------------------------------------------------
jira_url = os.getenv("JIRA_URL")
gemini_key = os.getenv("GEMINI_API_KEY")

if not jira_url or not gemini_key:
    print("🛑 STOP: Python cannot find your .env file or the passwords inside it!")
    print(
        "Please make sure your file is named EXACTLY '.env' and is in the main folder."
    )
    exit()

if not jira_url.startswith("http"):
    print(
        f"🛑 STOP: Your JIRA_URL must start with https:// (You currently have: {jira_url})"
    )
    exit()

# ---------------------------------------------------------
# TEST 1: Check Jira Connection
# ---------------------------------------------------------
try:
    print("Checking Jira...")
    jira = Jira(
        url=jira_url,
        username=os.getenv("JIRA_EMAIL"),
        password=os.getenv("JIRA_API_TOKEN"),
        cloud=True,
    )

    projects = jira.projects()
    print(f"✅ JIRA SUCCESS: Connected to {jira_url}")
    print(f"   Found {len(projects)} projects in your workspace.\n")

except Exception as e:
    print(
        f"❌ JIRA FAILED: Could not connect. Check your Atlassian API token.\nError details: {e}\n"
    )

# ---------------------------------------------------------
# TEST 2: Check Google Gemini Connection (New SDK)
# ---------------------------------------------------------
try:
    print("Checking Google Gemini...")
    # Using the new Google GenAI syntax
    client = genai.Client(api_key=gemini_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="In one short sentence, say 'Gemini is online and ready.'",
    )

    print("✅ GEMINI SUCCESS: The AI says ->", response.text)

except Exception as e:
    print(
        f"❌ GEMINI FAILED: Could not connect. Check your API key.\nError details: {e}"
    )
