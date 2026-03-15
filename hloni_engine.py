import os
import json
import math
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def calculate_structural_bill(size_sqm, building_type):
    # Logic for Steel & Electrical Estimation
    results = {}
    
    # 1. Electrical Prediction (SANS 10142)
    results['sockets'] = math.ceil(size_sqm / 12) * 2
    results['lights'] = math.ceil(size_sqm / 10)
    results['db_board'] = "24-Way Surface Mount" if size_sqm > 50 else "12-Way Flush Mount"
    results['coc_legal'] = "Mandatory. Qualified Electrician required for sign-off."

    # 2. Structural Steel Prediction
    # Estimating linear meters of steel based on 600mm stud spacing
    linear_meters = (size_sqm * 4.5) 
    results['steel_estimate_kg'] = round(linear_meters * 1.8, 2) # approx kg for lipless channel
    
    return results

def run_hloni_master_audit(user_data):
    size = float(user_data.get('size_sqm', 0))
    b_type = user_data.get('type', 'general') # e.g., 'office', 'ablution', 'classroom'
    users = int(user_data.get('expected_users', 1))

    # Basic Math Logic before AI refinement
    tech_specs = calculate_structural_bill(size, b_type)
    
    prompt = f"""
    You are Lehlonolo (Hloni). Perform a Pre-Inspection Audit for HMPD.co.za.
    
    USER PROJECT: {b_type}
    SIZE: {size} sqm
    USERS: {users}
    BUDGET: R{user_data.get('budget')}
    
    TECHNICAL PREDICTIONS:
    - Electrical: {tech_specs['lights']} lights, {tech_specs['sockets']} sockets, {tech_specs['db_board']}.
    - Steel Chassis/Frame: Approx {tech_specs['steel_estimate_kg']}kg.
    - Compliance: {tech_specs['coc_legal']}
    
    Based on SANS 10400 (Building), SANS 10142 (Electrical), and Civil Engineering standards for Chassis/Welding:
    1. Provide a detailed Dossier.
    2. Check if a CoC (Certificate of Compliance) is needed for this specific setup.
    3. If 'ablution', calculate EXACT toilets/basins for {users} users.
    4. Recommend Air Conditioning (BTU size) and Wall Sockets placement.
    5. Evaluate "Friction": If budget vs size is unrealistic, suggest Renovations.
    
    Identify as 'Hloni' and be extremely professional.
    """

    # AI Synthesis
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": "Master Industrial Auditor for HMPD."},
                  {"role": "user", "content": prompt}],
        model="llama3-70b-8192",
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    # Payload from the Website Floater
    payload = json.loads(os.environ.get("USER_PAYLOAD", "{}"))
    dossier = run_hloni_master_audit(payload)
    print(dossier)
