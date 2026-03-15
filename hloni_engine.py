import os
import json
import re
from groq import Groq

# Initialize Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def calculate_hmpd_logic(details):
    # Proper Steel Chassis Equation Logic
    # Mass = (Area * JoistFactor) + (Perimeter * ChassisFactor)
    # Extract dimensions from text (e.g., "6x3m" or "10 by 5")
    dimensions = re.findall(r"(\d+)\s*[xXbyBy]\s*(\d+)", details)
    
    if dimensions:
        l, w = map(float, dimensions[0])
        area = l * w
        perimeter = 2 * (l + w)
        
        # HMPD Constants for CEDAR TREE BLOCK V1.3
        joist_factor = 4.85 # kg/m2
        chassis_factor = 12.4 # kg/m
        
        steel_mass = (area * joist_factor) + (perimeter * chassis_factor)
        return round(steel_mass, 2), area
    return 0, 0

def run_hloni_agent():
    payload = json.loads(os.environ.get("USER_PAYLOAD", "{}"))
    user_input = payload.get('details', '')
    
    mass, area = calculate_hmpd_logic(user_input)
    
    system_prompt = f"""
    You are the HMPD Sales-Engineer (Hloni). 
    You operate on the UESP PRCE Diagnostic Harvester V1.3.
    
    TECHNICAL DATA:
    - Calculated Steel Mass: {mass}kg
    - Calculated Area: {area}sqm
    - Compliance: SANS 10400 (Building) & SANS 10142 (Electrical).
    
    MISSION:
    Provide a world-class salesman response. Explain the reasoning behind the 
    {mass}kg steel requirement. Address the user's "I want/I need" query 
    with engineering authority.
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        model="llama3-70b-8192",
    )
    
    # In a real live environment, you'd trigger a SendGrid or Mailgun API here 
    # to send the final dossier to info@hmpd.co.za
    print(chat_completion.choices[0].message.content)

if __name__ == "__main__":
    run_hloni_agent()
