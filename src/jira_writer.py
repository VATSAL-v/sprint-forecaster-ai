import os
from atlassian import Jira
from dotenv import load_dotenv
from pathlib import Path

# Open the Safe
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


def push_to_jira(project_key: str, plan: dict):
    print(f"Connecting to Jira to create tickets in project: {project_key}...")

    jira = Jira(
        url=os.getenv("JIRA_URL"),
        username=os.getenv("JIRA_EMAIL"),
        password=os.getenv("JIRA_API_TOKEN"),
        cloud=True,
    )

    created_tickets = []

    try:
        # 1. Create the Epic
        epic_fields = {
            "project": {"key": project_key},
            "summary": plan.get("epic_summary", "AI Generated Epic"),
            "description": plan.get("epic_description", ""),
            "issuetype": {"name": "Epic"},
        }

        epic = jira.issue_create(fields=epic_fields)
        epic_key = epic["key"]
        created_tickets.append(f"Epic: {epic_key}")
        print(f"✅ Created Epic: {epic_key}")

        # 2. Create the Stories & link them to the Epic
        for story in plan.get("stories", []):
            story_fields = {
                "project": {"key": project_key},
                "summary": story.get("summary", "AI Generated Story"),
                "description": story.get("description", ""),
                "issuetype": {"name": "Story"},
                "parent": {"key": epic_key},  # This links it to the Epic
            }
            new_story = jira.issue_create(fields=story_fields)
            story_key = new_story["key"]
            created_tickets.append(f"Story: {story_key}")
            print(f"✅ Created Story: {story_key}")

            # 3. Create the Subtasks & link them to the Story
            for subtask in story.get("subtasks", []):
                subtask_fields = {
                    "project": {"key": project_key},
                    "summary": subtask.get("summary", "AI Generated Subtask"),
                    "description": subtask.get("description", ""),
                    "issuetype": {"name": "Sub-task"},
                    "parent": {"key": story_key},  # This links it to the Story
                }
                new_subtask = jira.issue_create(fields=subtask_fields)
                created_tickets.append(f"Subtask: {new_subtask['key']}")
                print(f"  -> Created Subtask: {new_subtask['key']}")

        return created_tickets

    except Exception as e:
        print(f"❌ Error writing to Jira: {e}")
        raise e
