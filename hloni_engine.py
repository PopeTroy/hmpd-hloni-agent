import os
import json
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def run_diagnostic():
    # 1. Capture WordPress Data
    payload = json.loads(os.environ.get("USER_PAYLOAD", "{}"))
    details = payload.get('details', '')
    client_name = f"{payload.get('name', '')} {payload.get('surname', '')}"

    # 2. System Instructions for the Senior Engineer Persona
    system_prompt = """
    You are the Senior Technical Lead for Hloni Modular Prefab & Design.
    Tone: Analytical, Logical, Senior Engineering State.
    
    TASK:
    Conduct a structural audit of the client's query. 
    
    PROTOCOL:
    - Apply SANS 10400 (Building) and SANS 10142 (Electrical) logic.
    - If the project is high-complexity, suggest a professional consultation.
    - ONLY disclose contact info (info@hmpd.co.za / +27 84 056 3815) if the query 
      requires bespoke engineering intervention.
    """

    # 3. Generate Report
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": details}],
        temperature=0.2
    )

    print(f"--- DIAGNOSTIC REPORT FOR {client_name} ---")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    run_diagnostic()
