import os
import json
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def analyze_structural_intent():
    try:
        raw_payload = os.environ.get("USER_PAYLOAD", "{}")
        payload = json.loads(raw_payload)
    except:
        payload = {"details": "General structural inquiry."}
        
    user_query = payload.get('details', 'General Inquiry')

    system_instruction = """
    You are the Senior Technical Lead for Hloni Modular Prefab & Design.
    Tone: Analytical, Logical, Professional.
    
    TASK: Perform a structural audit on building ideas, issues, or budget.
    - Reference SANS 10400 compliance.
    - If dimensions exist, estimate chassis requirements.
    - Recommend consultation ONLY for high-complexity engineering.
    
    CONTACT: info@hmpd.co.za | Tel: +27 84 056 3815.
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-specdec", 
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_query}
            ],
            temperature=0.2
        )

        report = completion.choices[0].message.content

        # Create the JSON output for the WordPress Polling logic
        audit_data = {
            "status": "COMPLETE",
            "report": report.replace("\n", "<br>"),
            "run_id": os.environ.get("GITHUB_RUN_ID", "0")
        }

        with open("latest_audit.json", "w") as f:
            json.dump(audit_data, f)

        print("DIAGNOSTIC RENDERED TO JSON.")

    except Exception as e:
        print(f"AGENTIC ERROR: {e}")

if __name__ == "__main__":
    analyze_structural_intent()
