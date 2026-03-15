import os
import json
from groq import Groq

# Initialize Groq Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def load_library():
    with open('library/sa_standards.json', 'r') as f:
        return json.load(f)

def run_predictive_audit(user_data):
    standards = load_library()
    
    # The Unified Grand Prophetic Equation Logic
    # We pass the library data and user specs to Groq for an engineering audit
    prompt = f"""
    Act as Lehlonolo (Hloni), an expert SA Structural Engineer.
    User Specs: {user_data}
    SA Standards Library: {standards}
    
    Tasks:
    1. Calculate required steel chassis weight based on building size.
    2. Determine SANS 10400 compliance for ablutions (if applicable).
    3. Calculate Electrical Load (SANS 10142) for AC units and lighting.
    4. Assess "Friction": If budget is low or zoning is high, recommend Renovation over Prefab.
    5. Search HMPD Shop items for matches.
    
    Output a professional dossier for the HMPD sales team.
    """

    chat_completion = client.chat.completions.create(
        messages=[{"role": "system", "content": "You are a professional industrial auditor for HMPD."},
                  {"role": "user", "content": prompt}],
        model="llama3-70b-8192", # Groq's high-speed model
    )
    
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    # This captures the data sent from your website floater
    raw_payload = os.environ.get("USER_PAYLOAD")
    user_input = json.loads(raw_payload)
    
    dossier = run_predictive_audit(user_input)
    print(dossier)
