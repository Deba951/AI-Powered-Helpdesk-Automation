import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def classify_query(query):
    """
    Classify customer query into category, predict priority, generate response, and estimate confidence.

    Args:
        query (str): Customer query text

    Returns:
        dict: {
            'category': str,
            'priority': str,
            'response': str,
            'confidence': float
        }
    """
    prompt = f"""
    Analyze the following customer query and provide:
    1. Category: Choose from [Billing, Technical Issue, Product Inquiry, Feedback, General Inquiry]
    2. Priority: Choose from [Low, Medium, High] based on urgency
    3. Automated Response: A helpful response to the customer
    4. Confidence Score: A score from 0.0 to 1.0 indicating how confident you are in the classification

    Query: {query}

    Format your response as:
    Category: [category]
    Priority: [priority]
    Response: [response text]
    Confidence: [score]
    """

    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()

        # Parse the response
        lines = result_text.split('\n')
        category = ""
        priority = ""
        ai_response = ""
        confidence = 0.8  # Default confidence

        for line in lines:
            if line.startswith("Category:"):
                category = line.replace("Category:", "").strip()
            elif line.startswith("Priority:"):
                priority = line.replace("Priority:", "").strip()
            elif line.startswith("Response:"):
                ai_response = line.replace("Response:", "").strip()
            elif line.startswith("Confidence:"):
                try:
                    confidence = float(line.replace("Confidence:", "").strip())
                except ValueError:
                    confidence = 0.8

        # If parsing failed, provide defaults
        if not category:
            category = "General Inquiry"
        if not priority:
            priority = "Medium"
        if not ai_response:
            ai_response = "Thank you for your query. Our team will assist you shortly."

        return {
            'category': category,
            'priority': priority,
            'response': ai_response,
            'confidence': confidence
        }

    except Exception as e:
        print(f"Error in classification: {e}")
        return {
            'category': 'General Inquiry',
            'priority': 'Medium',
            'response': 'We apologize for the inconvenience. Please try again or contact support.',
            'confidence': 0.5
        }

# Test the function
if __name__ == "__main__":
    test_query = "I can't access my account after the recent update."
    result = classify_query(test_query)
    print("Test Result:")
    print(f"Category: {result['category']}")
    print(f"Priority: {result['priority']}")
    print(f"Response: {result['response']}")
    print(f"Confidence: {result['confidence']}")
