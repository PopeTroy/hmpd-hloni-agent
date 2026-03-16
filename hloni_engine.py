import os
import json
from groq import Groq

# Initialize Groq Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def analyze_structural_intent():
    # Set a default response in case of total failure
    report = "System Error: The Senior Engine could not synthesize a report at this time."
    
    try:
        raw_payload = os.environ.get("USER_PAYLOAD", "{}")
        payload = json.loads(raw_payload)
        user_query = payload.get('details', 'General Inquiry')

        # Updated to the current supported model: llama-3.3-70b-versatile
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are the Senior Technical Lead for Hloni Modular Prefab & Design. "
                        "Persona: Analytical, Logical, Professional. "
                        "TASK: Perform a structural audit on building ideas, issues, or budget. "
                        "Reference SANS 10400 compliance. "
                        "Contact: info@hmpd.co.za | Tel: +27 84 056 3815."
                    )
                },
                {"role": "user", "content": user_query}
            ],
            temperature=0.2
        )
        report = completion.choices[0].message.content

    except Exception as e:
        print(f"Error: {e}")
        report = f"Diagnostic Interrupted: {str(e)}"

    # CRITICAL: Always write the file so Git doesn't fail with Exit 128
    audit_data = {
        "status": "COMPLETE",
        "report": report.replace("\n", "<br>"),
        "run_id": os.environ.get("GITHUB_RUN_ID", "0")
    }

    with open("latest_audit.json", "w") as f:
        json.dump(audit_data, f)
    
    print("UESP PRCE DIAGNOSTIC RENDERED SUCCESSFULLY.")

if __name__ == "__main__":
    analyze_structural_intent()
