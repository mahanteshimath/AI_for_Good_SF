import streamlit as st
import json
import google.generativeai as genai
import pytesseract
from PIL import Image
import io
import fitz  # PyMuPDF for PDF processing



# Accessing the database credentials
db_credentials = st.secrets["db_credentials"]
if 'google_api_key' not in st.session_state:
    st.session_state.google_api_key = db_credentials["google_api_key"]


genai.configure(api_key=st.session_state.google_api_key)
model = genai.GenerativeModel('gemini-1.5-flash')



def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    try:
        pdf_bytes = pdf_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

def extract_text_from_image(image_file):
    """Extract text from image using OCR"""
    try:
        image = Image.open(image_file)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

def analyze_bridge_plan(plan_text, uploaded_images=None):
    # Construct the prompt based on available data
    base_prompt = """
    As a civil engineering expert, analyze the following bridge development plan. 
    Consider these key aspects:
    1. Structural integrity and safety
    2. Environmental impact
    3. Cost efficiency
    4. Construction timeline
    5. Maintenance requirements
    6. Potential risks and mitigation strategies
    
    Provide a detailed analysis with specific recommendations.
    """
    
    if uploaded_images:
        base_prompt += "\nAnalysis includes insights from visual bridge plan documents."
    
    base_prompt += f"\nBridge Plan:\n{plan_text}"
    
    base_prompt += """
    Format the response as a JSON with the following structure:
    {
        "overall_assessment": "summary of analysis",
        "structural_analysis": {
            "strengths": [],
            "concerns": [],
            "recommendations": []
        },
        "environmental_impact": {
            "positive_impacts": [],
            "negative_impacts": [],
            "mitigation_strategies": []
        },
        "cost_analysis": {
            "efficiency_rating": "1-10",
            "cost_saving_opportunities": [],
            "budget_risks": []
        },
        "timeline_assessment": {
            "estimated_duration": "",
            "potential_delays": [],
            "optimization_suggestions": []
        },
        "maintenance_plan": {
            "frequency": "",
            "key_requirements": [],
            "estimated_costs": ""
        },
        "risk_assessment": {
            "critical_risks": [],
            "mitigation_strategies": [],
            "contingency_plans": []
        }
    }
    """
    
    response = model.generate_content(base_prompt)
    try:
        return json.loads(response.text)
    except Exception as e:
        st.error(f"Error parsing AI response: {str(e)}")
        return None



# App title and description
st.title("🌉 Bridge Development Plan Analyzer")
st.write("""
This AI-powered tool analyzes bridge development plans and provides comprehensive 
insights on structural integrity, environmental impact, costs, timeline, and risks.
""")

# File upload
uploaded_files = st.file_uploader(
    "Upload your bridge development plan (PDF, TXT, or JPEG)", 
    type=["pdf", "txt", "jpeg", "jpg"],
    accept_multiple_files=True
)

# Text input as alternative
plan_text = st.text_area(
    "Or paste your plan text here:",
    height=200,
    placeholder="Enter the bridge development plan details..."
)

# Initialize list to store uploaded images
uploaded_images = []

if uploaded_files:
    plan_text_parts = []
    
    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/pdf":
            pdf_text = extract_text_from_pdf(uploaded_file)
            if pdf_text:
                plan_text_parts.append(pdf_text)
                
        elif uploaded_file.type.startswith("image/"):
            # Display the uploaded image
            st.image(uploaded_file, caption="Uploaded Bridge Plan Image", use_column_width=True)
            # Extract text from image
            image_text = extract_text_from_image(uploaded_file)
            if image_text:
                plan_text_parts.append(image_text)
            # Store image for potential further use
            uploaded_images.append(uploaded_file)
            
        else:  # Text files
            text_content = uploaded_file.getvalue().decode("utf-8")
            plan_text_parts.append(text_content)
    
    # Combine all text parts
    if plan_text_parts:
        plan_text = "\n\n".join(plan_text_parts)

if st.button("Analyze Plan", disabled=not (plan_text or uploaded_files)):
    with st.spinner("Analyzing your bridge development plan..."):
        # Pass uploaded_images instead of image_data
        analysis = analyze_bridge_plan(plan_text, uploaded_images)
        if analysis:
            display_analysis(analysis)
