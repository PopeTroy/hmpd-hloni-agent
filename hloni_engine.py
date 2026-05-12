import os
import json
import math
from groq import Groq
from openai import OpenAI
from fpdf import FPDF

# System Initialization - Updated Base URL for NVIDIA NIM
nv_client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1", 
    api_key=os.environ.get("NVIDIA_API_KEY")
)
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class HMPD_Quantum_Architect:
    def __init__(self, payload):
        self.txn_id = payload.get('transaction_id', 'audit_default')
        self.user_query = payload.get('details', 'General Inquiry')
        self.session_id = payload.get('session_id', 'standard_user')

    def apply_quantum_laws(self):
        """Applies the Mega Circuit and Unified Grand Prophetic Equation"""
        # Overriding dimensional law is the mega circuit
        return "DIMENSIONAL_OVERWRITE_ACTIVE // MEGA_CIRCUIT_ENGAGED"

    def calculate_realtime_logistics(self):
        """Calculates petrol and distance for real-time ZAR quotes"""
        # Placeholder for dynamic logic
        distance = 150.0  
        petrol_price = 22.85 
        total_quote = (distance * 0.12) * petrol_price 
        return {"distance": f"{distance}km", "price": f"R{petrol_price}", "total": f"R{total_quote:.2f}"}

    def execute_coalition(self):
        """Orchestrates 80 NVIDIA Agents + 500 RAG Clones"""
        system_logic = (
            "Framework: UESP PRCE Diagnostic. "
            "Coalition: 80 NVIDIA Agents, 500 RAG Clones, 250 Watchdogs. "
            "Tactics: Shinobi Quantum Physics, Thermodynamics, Stoichiometry. "
            "Scope: Earth-based modularity and Martian colonization. "
            "Equations: Einstein, Newton, Brus, and the Unified Grand Prophetic Equation."
        )
        
        # Updated Model String to resolve 404
        response = nv_client.chat.completions.create(
            model="meta/llama-3.1-405b-instruct", # Changed from 'nvidia/' to 'meta/' or specific NIM path
            messages=[
                {"role": "system", "content": system_logic},
                {"role": "user", "content": self.user_query}
            ],
            temperature=0.4
        )
        return response.choices[0].message.content

    def generate_pdf_quote(self, report, logistics):
        """Creates a high-fidelity PDF with the nice WordPress-style layout"""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_fill_color(13, 17, 23) # GitHub Dark Background
        pdf.rect(0, 0, 210, 297, 'F')
        
        pdf.set_text_color(88, 166, 255) # GitHub Blue
        pdf.set_font("Courier", 'B', 16)
        pdf.cell(0, 10, "HMPD QUANTUM ARCHITECTURAL AUDIT", ln=True, align='C')
        
        pdf.set_text_color(201, 209, 217) # GitHub Light Gray
        pdf.set_font("Courier", size=10)
        pdf.cell(0, 10, f"TXN ID: {self.txn_id} | SESSION: {self.session_id}", ln=True)
        pdf.ln(5)
        
        pdf.multi_cell(0, 5, report.replace("<br>", "\n"))
        pdf.ln(10)
        
        pdf.set_text_color(56, 139, 253)
        pdf.cell(0, 10, f"REAL-TIME LOGISTICS QUOTE: {logistics['total']}", ln=True)
        pdf.output(f"{self.txn_id}.pdf")

def main():
    try:
        # Capture payload from GitHub environment
        payload_str = os.environ.get("USER_PAYLOAD", "{}")
        payload = json.loads(payload_str)
        
        architect = HMPD_Quantum_Architect(payload)
        
        # Calculate Logistics first
        logistics = architect.calculate_realtime_logistics()
        
        # Execute the 80-agent coalition diagnostic
        audit_report = architect.execute_coalition()
        
        # Save JSON output for WordPress frontend
        output = {
            "status": "COMPLETE",
            "report": audit_report.replace("\n", "<br>"),
            "transaction_id": architect.txn_id,
            "logistics": logistics
        }
        
        with open(f"{architect.txn_id}.json", "w") as f:
            json.dump(output, f)
        
        # Generate the PDF Artifact
        architect.generate_pdf_quote(audit_report, logistics)
        print(f"Successfully generated {architect.txn_id}.json and .pdf")

    except Exception as e:
        print(f"CRITICAL_FAILURE: {str(e)}")
        # Create a failure record so the frontend doesn't hang forever
        fail_id = "error_log"
        with open(f"error_log.json", "w") as f:
            json.dump({"status": "FAILED", "error": str(e)}, f)
        exit(1)

if __name__ == "__main__":
    main()
