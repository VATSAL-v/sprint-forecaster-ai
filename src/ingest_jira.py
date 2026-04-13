import os
import json
from atlassian import Jira
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


def fetch_jira_tickets():
    print("Connecting to Jira...")
    jira = Jira(
        url=os.getenv("JIRA_URL"),
        username=os.getenv("JIRA_EMAIL"),
        password=os.getenv("JIRA_API_TOKEN"),
        cloud=True,
    )

    # The custom JQL for your specific user and project scope
    jql_query = "reporter = 5ed00cbebc087d0c260737cc AND type IN (Story, Sub-task) AND project IN (APP, WORK) ORDER BY created DESC"

    all_issues = []
    target_total = 1000  # The optimal number of tickets for our MVP

    print(f"Executing JQL: {jql_query}")
    print(f"Attempting to fetch up to {target_total} tickets in batches...")

    # The New Pagination Loop for Jira Cloud
    is_last = False
    next_page_token = None
    batch_count = 1

    while not is_last and len(all_issues) < target_total:
        print(f"Fetching batch {batch_count}...")

        # enhanced_jql is the new required method for Jira Cloud
        response = jira.enhanced_jql(jql_query, nextPageToken=next_page_token)

        issues = response.get("issues", [])
        if not issues:
            print("No more tickets found in Jira matching this query.")
            break

        all_issues.extend(issues)

        # Atlassian now uses tokens instead of start/limit logic
        is_last = response.get("isLast", True)
        next_page_token = response.get("nextPageToken")
        batch_count += 1

        # Stop if we hit our target
        if len(all_issues) >= target_total:
            all_issues = all_issues[:target_total]
            break

    print(f"✅ Successfully fetched {len(all_issues)} tickets.")

    # Save to JSON
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    file_path = data_dir / "jira_tickets.json"

    # Extract just the useful fields to save space
    cleaned_issues = []
    for issue in all_issues:
        cleaned_issues.append(
            {
                "key": issue["key"],
                "summary": issue["fields"]["summary"],
                "description": issue["fields"].get("description") or "",
                "issuetype": issue["fields"]["issuetype"]["name"],
            }
        )

    with open(file_path, "w") as f:
        json.dump(cleaned_issues, f, indent=4)

    print(f"✅ Data saved to {file_path}")


if __name__ == "__main__":
    fetch_jira_tickets()
