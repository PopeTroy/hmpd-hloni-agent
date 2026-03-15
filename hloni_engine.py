import os
import json
import re
from groq import Groq

# Initialize Groq Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def analyze_structural_intent():
    # 1. Capture the WordPress Handshake
    try:
        payload = json.loads(os.environ.get("USER_PAYLOAD", "{}"))
    except:
        payload = {"details": "No data received."}
        
    user_query = payload.get('details', '')

    # 2. Senior State System Prompt
    system_instruction = """
    You are the Senior Technical Lead for Hloni Modular Prefab & Design.
    Your persona is analytical, logical, and highly professional.
    
    TASK: 
    Perform a structural audit based on the user's building ideas, issues, or budget.
    
    LOGIC PROTOCOL:
    - Identify if the query involves a 'Budget', 'Building Idea', or 'Structural Issue'.
    - Apply SANS 10400 compliance reasoning.
    - If the query mentions specific dimensions, calculate a rough modular chassis requirement.
    - If the complexity is high, formally recommend a consultation.
    
    CONTACT DISCLOSURE RULE:
    Only suggest direct contact if the logic proves that bespoke engineering is required.
    Contact: info@hmpd.co.za | Tel: +27 84 056 3815.
    """

    # 3. Agentic Processing
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_query}
        ],
        temperature=0.2 # Keep it analytical and consistent
    )

    report = completion.choices[0].message.content

    # 4. Final Rendering (This is what the GitHub Log will show)
    print("--------------------------------------------------")
    print("UESP PRCE SENIOR STATE DIAGNOSTIC REPORT")
    print("--------------------------------------------------")
    print(report)
    print("--------------------------------------------------")
    print("AUDIT COMPLETE: DISPATCHED TO HMPD CORE.")

if __name__ == "__main__":
    analyze_structural_intent()
