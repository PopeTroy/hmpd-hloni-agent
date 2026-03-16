import os
import json
from groq import Groq

# Initialize Groq Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def analyze_structural_intent():
    # 1. Capture the WordPress Handshake
    try:
        raw_payload = os.environ.get("USER_PAYLOAD", "{}")
        payload = json.loads(raw_payload)
    except Exception as e:
        print(f"Error parsing payload: {e}")
        payload = {"details": "No data received."}
        
    user_query = payload.get('details', 'General Inquiry')

    # 2. Senior State System Prompt
    system_instruction = """
    You are the Senior Technical Lead for Hloni Modular Prefab & Design.
    Persona: Analytical, Logical, and highly professional.
    
    TASK: 
    Perform a structural audit based on building ideas, issues, or budget.
    
    LOGIC PROTOCOL:
    - Identify if the query involves a 'Budget', 'Building Idea', or 'Structural Issue'.
    - Apply SANS 10400 compliance reasoning.
    - If complexity is high, formally recommend a consultation.
    
    CONTACT DISCLOSURE RULE:
    Only suggest direct contact if the logic proves bespoke engineering is required.
    Contact: info@hmpd.co.za | Tel: +27 84 056 3815.
    """

    try:
        # 3. Agentic Processing - UPDATED MODEL NAME
        completion = client.chat.completions.create(
            model="llama-3.3-70b-specdec", 
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_query}
            ],
            temperature=0.2
        )

        report = completion.choices[0].message.content

        # 4. Final Rendering
        print("--------------------------------------------------")
        print("UESP PRCE SENIOR STATE DIAGNOSTIC REPORT")
        print("--------------------------------------------------")
        print(report)
        print("--------------------------------------------------")
        print("AUDIT COMPLETE: DISPATCHED TO HMPD CORE.")

    except Exception as e:
        print(f"AGENTIC ERROR: Structural Engine failed to synthesize data. {e}")

if __name__ == "__main__":
    analyze_structural_intent()
