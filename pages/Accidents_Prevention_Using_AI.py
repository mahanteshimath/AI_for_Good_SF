import streamlit as st
import json
import google.generativeai as genai
import pytesseract
from PIL import Image
import io
import fitz  # PyMuPDF for PDF processing

# # Configure page settings
# st.set_page_config(
#     page_title="Bridge Development Plan Analyzer",
#     page_icon="🌉",
#     layout="wide"
# )


db_credentials = st.secrets["db_credentials"]
google_api_key = db_credentials["google_api_key"]
# Initialize Gemini
if 'google_api_key' not in st.secrets:
    st.error("Please add your Google API key to the secrets.")
    st.stop()

genai.configure(api_key=st.secrets['google_api_key'])
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

def analyze_bridge_plan(plan_text, image_data=None):
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
    
    if image_data:
        base_prompt += "\nAnalysis includes visual inspection of provided bridge plan images."
    
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
    except:
        st.error("Error parsing AI response. Please try again.")
        return None

def display_analysis(analysis):
    if not analysis:
        return
    
    # Overall Assessment
    st.header("Overall Assessment")
    st.write(analysis["overall_assessment"])
    
    # Structural Analysis
    with st.expander("Structural Analysis", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Strengths")
            for strength in analysis["structural_analysis"]["strengths"]:
                st.success(strength)
        with col2:
            st.subheader("Concerns")
            for concern in analysis["structural_analysis"]["concerns"]:
                st.warning(concern)
        with col3:
            st.subheader("Recommendations")
            for rec in analysis["structural_analysis"]["recommendations"]:
                st.info(rec)
    
    # Environmental Impact
    with st.expander("Environmental Impact"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Impacts")
            for impact in analysis["environmental_impact"]["positive_impacts"]:
                st.success(f"✓ {impact}")
            for impact in analysis["environmental_impact"]["negative_impacts"]:
                st.error(f"✗ {impact}")
        with col2:
            st.subheader("Mitigation Strategies")
            for strategy in analysis["environmental_impact"]["mitigation_strategies"]:
                st.info(strategy)
    
    # Cost Analysis
    with st.expander("Cost Analysis"):
        st.metric("Efficiency Rating", f"{analysis['cost_analysis']['efficiency_rating']}/10")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Cost Saving Opportunities")
            for opp in analysis["cost_analysis"]["cost_saving_opportunities"]:
                st.success(opp)
        with col2:
            st.subheader("Budget Risks")
            for risk in analysis["cost_analysis"]["budget_risks"]:
                st.warning(risk)
    
    # Timeline Assessment
    with st.expander("Timeline Assessment"):
        st.metric("Estimated Duration", analysis["timeline_assessment"]["estimated_duration"])
        st.subheader("Potential Delays")
        for delay in analysis["timeline_assessment"]["potential_delays"]:
            st.warning(delay)
        st.subheader("Optimization Suggestions")
        for suggestion in analysis["timeline_assessment"]["optimization_suggestions"]:
            st.info(suggestion)
    
    # Maintenance Plan
    with st.expander("Maintenance Plan"):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Maintenance Frequency", analysis["maintenance_plan"]["frequency"])
            st.metric("Estimated Costs", analysis["maintenance_plan"]["estimated_costs"])
        with col2:
            st.subheader("Key Requirements")
            for req in analysis["maintenance_plan"]["key_requirements"]:
                st.write(f"• {req}")
    
    # Risk Assessment
    with st.expander("Risk Assessment"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Critical Risks")
            for risk in analysis["risk_assessment"]["critical_risks"]:
                st.error(risk)
        with col2:
            st.subheader("Mitigation Strategies")
            for strategy in analysis["risk_assessment"]["mitigation_strategies"]:
                st.success(strategy)
        st.subheader("Contingency Plans")
        for plan in analysis["risk_assessment"]["contingency_plans"]:
            st.info(plan)

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

if uploaded_files:
    plan_text_parts = []
    image_data = []
    
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
            # Store image data for analysis
            image_data.append(uploaded_file)
            
        else:  # Text files
            text_content = uploaded_file.getvalue().decode("utf-8")
            plan_text_parts.append(text_content)
    
    # Combine all text parts
    if plan_text_parts:
        plan_text = "\n\n".join(plan_text_parts)

if st.button("Analyze Plan", disabled=not (plan_text or uploaded_files)):
    with st.spinner("Analyzing your bridge development plan..."):
        analysis = analyze_bridge_plan(plan_text, image_data)
        if analysis:
            display_analysis(analysis)
