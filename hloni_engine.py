import os
import json
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def analyze_structural_intent():
    try:
        raw_payload = os.environ.get("USER_PAYLOAD", "{}")
        payload = json.loads(raw_payload)
        user_query = payload.get('details', 'General Inquiry')
        # CAPTURE THE UNIQUE ID
        txn_id = payload.get('transaction_id', 'audit_default')

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[
                {"role": "system", "content": "You are the Senior Technical Lead for Hloni Modular Prefab & Design. Perform a structural audit."},
                {"role": "user", "content": user_query}
            ],
            temperature=0.7 # Higher temperature ensures more unique phrasing per run
        )
        report = completion.choices[0].message.content

        audit_data = {
            "status": "COMPLETE",
            "report": report.replace("\n", "<br>"),
            "transaction_id": txn_id
        }

        # SAVE AS UNIQUE FILENAME
        with open(f"{txn_id}.json", "w") as f:
            json.dump(audit_data, f)
        
        print(f"SUCCESS: Audit saved as {txn_id}.json")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_structural_intent()
