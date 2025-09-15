import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API configuration
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = os.getenv("API_PORT", "8000")
API_URL = f"http://{API_HOST}:{API_PORT}"

st.set_page_config(
    page_title="AI-Powered Helpdesk Automation",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI-Powered Helpdesk Automation")
st.markdown("Test the AI model for customer query classification and automated responses.")

# Input section
st.header("Customer Query Input")

col1, col2 = st.columns(2)

with col1:
    customer_name = st.text_input("Customer Name", placeholder="Enter customer name")

with col2:
    query = st.text_area("Customer Query", placeholder="Enter the customer's query here...", height=100)

# Escalation checkbox
escalate_case = st.checkbox("🚨 Escalate this case to human agent", help="If checked, the case will be marked as 'Open' in Salesforce for agent handling")

# Predict button
if st.button("🔍 Analyze Query", type="primary"):
    if not customer_name.strip():
        st.error("Please enter a customer name.")
    elif not query.strip():
        st.error("Please enter a customer query.")
    else:
        with st.spinner("Analyzing query with AI and creating Salesforce case..."):
            try:
                # Make API request to create case
                response = requests.post(
                    f"{API_URL}/create_case",
                    json={
                        "customer_name": customer_name.strip(),
                        "query": query.strip(),
                        "escalated": escalate_case
                    },
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()

                    # Display results
                    st.success("✅ Analysis Complete!")

                    # Results in columns
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("📂 Category", result['category'])

                    with col2:
                        priority_color = {
                            "Low": "🟢",
                            "Medium": "🟡",
                            "High": "🔴"
                        }
                        st.metric("⚡ Priority", f"{priority_color.get(result['priority'], '⚪')} {result['priority']}")

                    with col3:
                        st.metric("🎯 Confidence", f"{result['confidence']:.2%}")

                    # AI Response
                    st.header("💬 AI-Generated Response")
                    st.info(result['response'])

                    # Salesforce Integration Status
                    st.header("☁️ Salesforce Integration")
                    if result.get('salesforce_case_id'):
                        st.success(f"✅ Case created successfully in Salesforce!")
                        st.code(f"Case ID: {result['salesforce_case_id']}")
                        st.code(f"Status: {result['salesforce_status']}")
                        if result['escalated']:
                            st.warning("🚨 This case has been escalated and is now open for agent handling.")
                        else:
                            st.info("📋 Case is closed (auto-resolved by AI).")
                    else:
                        st.error("❌ Failed to create Salesforce case. Check credentials and connection.")

                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"Connection Error: {str(e)}")
                st.info("Make sure the API server is running on the configured host and port.")

# Sidebar with information
st.sidebar.header("ℹ️ About")
st.sidebar.markdown("""
This application demonstrates an AI-powered helpdesk system that:
- **Classifies** customer queries into categories
- **Predicts** priority levels
- **Generates** automated responses
- **Integrates** with Salesforce CRM

**Categories:** Billing, Technical Issue, Product Inquiry, Feedback, General Inquiry
**Priority Levels:** Low, Medium, High
""")

st.sidebar.header("🔧 Configuration")
st.sidebar.code(f"API URL: {API_URL}")
st.sidebar.code(f"Model: Gemini 1.5 Flash")

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit, FastAPI, and Google Gemini AI*")
