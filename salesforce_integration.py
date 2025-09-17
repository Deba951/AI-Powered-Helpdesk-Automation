import os
from simple_salesforce.api import Salesforce
from dotenv import load_dotenv
from typing import Any

# Load environment variables
load_dotenv()

class SalesforceIntegration:
    # Initializes the Salesforce connection when an object is created.
    def __init__(self):
        self.sf: Any = None  # type: ignore
        self.connect()

    # Taking credentials from .env file to connect to Salesforce
    def connect(self):
        """Connect to Salesforce using credentials from environment variables."""
        try:
            self.sf = Salesforce(
                username=os.getenv('SALESFORCE_USERNAME'),
                password=os.getenv('SALESFORCE_PASSWORD'),
                security_token=os.getenv('SALESFORCE_SECURITY_TOKEN'),
                domain=os.getenv('SALESFORCE_DOMAIN', 'login')
            )
            print("Successfully connected to Salesforce")
        except Exception as e:
            print(f"Failed to connect to Salesforce: {e}")
            self.sf = None

    # Creating the Case
    def create_case(self, customer_name, query, category, priority, ai_response, escalated=False):
        """
        Create a new Case record in Salesforce.

        Args:
            customer_name (str): Name of the customer
            query (str): Original customer query
            category (str): Predicted category
            priority (str): Predicted priority
            ai_response (str): AI-generated response
            escalated (bool): Whether the case should be escalated

        Returns:
            dict: Case creation result or error
        """
        if not self.sf:
            return {"success": False, "error": "Not connected to Salesforce"}

        # If escalated, marks the Case as open
        try:
            # Determine status based on escalation
            status = "Open" if escalated else "Closed"

            # Map priority to Salesforce format
            sf_priority = {
                "Low": "Low",
                "Medium": "Medium",
                "High": "High"
            }.get(priority, "Medium")

            # Create a dictionary case_data with all required fields.
            case_data = {
                "Subject": f"AI Helpdesk: {category} - {customer_name}",
                "Description": f"Customer Query: {query}\n\nAI Response: {ai_response}",
                "Status": status,
                "Priority": sf_priority,
                "Origin": "AI Helpdesk",
                "Type": category,
                "SuppliedName": customer_name,
                "SuppliedEmail": "",  # Can be added later if available
                "SuppliedPhone": "",  # Can be added later if available
                # Custom fields for AI predictions
                "AI_Predicted_Category__c": category,
                "AI_Predicted_Priority__c": priority,
                "AI_Response__c": ai_response,
                "Escalated__c": escalated
            }

            # create the case
            result = self.sf.Case.create(case_data)  # type: ignore
            return {"success": True, "case_id": result['id'], "status": status}

        except Exception as e:
            print(f"Error creating case: {e}")
            return {"success": False, "error": str(e)}

    # Updates the Status field of a case using its case_id.
    def update_case_status(self, case_id, status):
        """Update the status of an existing case."""
        if not self.sf:
            return {"success": False, "error": "Not connected to Salesforce"}

        try:
            self.sf.Case.update(case_id, {"Status": status})  # type: ignore
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_case_details(self, case_id):
        """Retrieve case details."""
        if not self.sf:
            return {"success": False, "error": "Not connected to Salesforce"}

        try:
            case = self.sf.Case.get(case_id)  # type: ignore
            return {"success": True, "case": case}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # Creates a task linked to a case (WhatId). Optionally assigns it to a user (OwnerId).
    def create_task(self, case_id, subject, description, assigned_to=None):
        """Create a task related to a case."""
        if not self.sf:
            return {"success": False, "error": "Not connected to Salesforce"}

        try:
            task_data = {
                "Subject": subject,
                "Description": description,
                "WhatId": case_id,  # Link to the case
                "Status": "Not Started",
                "Priority": "Normal"
            }
            if assigned_to:
                task_data["OwnerId"] = assigned_to

            result = self.sf.Task.create(task_data)  # type: ignore
            return {"success": True, "task_id": result['id']}
        except Exception as e:
            return {"success": False, "error": str(e)}

# Global instance
sf_integration = SalesforceIntegration()

# Verifies if the connection is successful. Runs a sample query to fetch 5 cases
def test_salesforce_connection():
    """Test function to verify Salesforce connection."""
    if sf_integration.sf:
        print("✅ Salesforce connection successful")
        # Try to query cases
        try:
            cases = sf_integration.sf.query("SELECT Id, Subject FROM Case LIMIT 5")
            print(f"Found {cases['totalSize']} cases")
        except Exception as e:
            print(f"Query failed: {e}")
    else:
        print("❌ Salesforce connection failed")

if __name__ == "__main__":
    test_salesforce_connection()
