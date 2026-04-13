import json
from pathlib import Path

# 1. Define file paths
data_dir = Path(__file__).parent.parent / "data"
input_file = data_dir / "raw_jira_tickets.json"
output_file = data_dir / "scrubbed_jira_tickets.json"

# 2. Define our sanitization dictionary (Employee names, specific SDKs, etc.)
replacements = {
    "YinzCam": "TechCorp",
    "yinzcam.com": "techcorp.com",
    "vatsal.vajani": "tpm.user",
    "Vatsal": "TPM",
    "Ticketmaster": "VendorAuth",
    "TM SDK": "Vendor SDK",
    # Note: We left the Tricodes out so they remain authentic!
}


def redact_descriptions(data):
    """Recursively hunts through the JSON to find and redact descriptions."""
    if isinstance(data, dict):
        for key, value in data.items():
            if key.lower() == "description":
                # Overwrite the sensitive data with a safe placeholder
                data[key] = (
                    "[Proprietary technical implementation details redacted for privacy.]"
                )
            else:
                redact_descriptions(value)
    elif isinstance(data, list):
        for item in data:
            redact_descriptions(item)
    return data


def scrub_data():
    print("Starting enterprise data sanitization...")

    try:
        # Step 1: Load the JSON safely
        with open(input_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        # Step 2: Hunt down and destroy all sensitive descriptions
        redacted_json = redact_descriptions(json_data)

        # Step 3: Convert back to text to do the name/SDK swaps
        json_text = json.dumps(redacted_json)
        for sensitive, generic in replacements.items():
            json_text = json_text.replace(sensitive, generic)

        # Step 4: Save the fully scrubbed data
        final_json = json.loads(json_text)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(final_json, f, indent=4)

        print(
            f"✅ Success! Descriptions redacted and data saved to: {output_file.name}"
        )

    except FileNotFoundError:
        print(
            f"❌ Error: Could not find {input_file.name}. Make sure it is in the data folder."
        )
    except json.JSONDecodeError:
        print("❌ Error: The raw file is not valid JSON.")


if __name__ == "__main__":
    scrub_data()
