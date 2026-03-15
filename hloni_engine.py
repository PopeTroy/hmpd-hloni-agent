import os
import json
from groq import Groq

# Initialize the Engine
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def analyze_complexity(details):
    """
    Analyzes if the query requires a 'Professional Senior State' intervention.
    """
    complex_triggers = ['industrial', 'multi-story', 'coastal', 'sanitary', 'foundation', 'solar']
    needs_hloni = any(word in details.lower() for word in complex_triggers)
    return needs_hloni

def run_hloni_audit():
    # Capture the payload from the WordPress Dispatch
    payload = json.loads(os.environ.get("USER_PAYLOAD", "{}"))
    user_query = payload.get('details', 'No details provided.')
    user_name = payload.get('name', 'Client')
    
    # 1. THE HEAVY LIFTING: Structural Logic
    # (Using the HMPD Area-to-Steel Mass Equation)
    # logic_mass = calculated_area * joist_constant...
    
    # 2. THE AGENTIC RESPONSE (Synthesized via Groq)
    system_instruction = f"""
    You are the Senior Technical Lead for Hloni Modular Prefab & Design.
    Your tone is analytical, logical, and professional. 
    
    ROLE:
    Evaluate the client's request: '{user_query}'.
    
    PROTOCOL:
    1. If the query is a standard modular request, provide the structural audit.
    2. If the query involves technical complexities (SANS compliance, structural loads, etc.), 
       formally suggest a professional consultation.
    
    CONTACT DISCLOSURE RULE:
    Only provide contact details if the diagnostic reveals a need for bespoke engineering. 
    In those cases, refer them to info@hmpd.co.za or tel:+0840563815. 
    Otherwise, focus strictly on the structural report.
    """

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "system", "content": system_instruction},
                  {"role": "user", "content": user_query}],
        temperature=0.3
    )

    report_content = completion.choices[0].message.content

    # 3. TRIGGER FINAL TRANSMISSION (Email to info@hmpd.co.za)
    # This part would interface with an SMTP action or SendGrid to 
    # forward the final dossier.
    print(f"DIAGNOSTIC REPORT GENERATED FOR: {user_name}")
    print("-" * 30)
    print(report_content)

if __name__ == "__main__":
    run_hloni_audit()
