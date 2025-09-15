#!/usr/bin/env python3
"""
Test script to verify Salesforce connection and credentials.
Run this script to check if your Salesforce integration is working correctly.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_env_variables():
    """Test if all required environment variables are set."""
    print("🔍 Checking environment variables...")

    required_vars = [
        'SALESFORCE_USERNAME',
        'SALESFORCE_PASSWORD',
        'SALESFORCE_SECURITY_TOKEN',
        'SALESFORCE_DOMAIN'
    ]

    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.strip() == '':
            missing_vars.append(var)
        else:
            # Mask sensitive information
            if 'PASSWORD' in var or 'TOKEN' in var:
                print(f"✅ {var}: {'*' * len(value)}")
            else:
                print(f"✅ {var}: {value}")

    if missing_vars:
        print(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please update your .env file with the correct values.")
        return False

    print("\n✅ All environment variables are set!")
    return True

def test_salesforce_connection():
    """Test the actual Salesforce connection."""
    print("\n🔌 Testing Salesforce connection...")

    try:
        from salesforce_integration import sf_integration

        if sf_integration.sf:
            print("✅ Successfully connected to Salesforce!")

            # Try to query some cases
            try:
                cases = sf_integration.sf.query("SELECT Id, Subject, Status FROM Case LIMIT 5")
                print(f"📊 Found {cases['totalSize']} cases in your org")

                if cases['totalSize'] > 0:
                    print("📋 Recent cases:")
                    for case in cases['records']:
                        print(f"  - {case['Subject']} ({case['Status']})")

            except Exception as e:
                print(f"⚠️  Could query cases: {e}")
                print("This might be normal if you have no cases or restricted permissions.")

            return True
        else:
            print("❌ Failed to connect to Salesforce")
            print("Please check your credentials and try again.")
            return False

    except ImportError:
        print("❌ Could not import salesforce_integration module")
        print("Make sure you're running this from the project directory.")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_case_creation():
    """Test creating a sample case."""
    print("\n📝 Testing case creation...")

    try:
        from salesforce_integration import sf_integration

        # Create a test case
        result = sf_integration.create_case(
            customer_name="Test Customer",
            query="This is a test query for connection verification",
            category="General Inquiry",
            priority="Low",
            ai_response="This is a test response from the AI system.",
            escalated=False
        )

        if result['success']:
            print("✅ Test case created successfully!")
            print(f"📋 Case ID: {result['case_id']}")
            print(f"📊 Status: {result['status']}")

            # Clean up - delete the test case
            try:
                sf_integration.sf.Case.delete(result['case_id'])
                print("🗑️  Test case cleaned up")
            except Exception as e:
                print(f"⚠️  Could not delete test case: {e}")

            return True
        else:
            print(f"❌ Failed to create test case: {result['error']}")
            return False

    except Exception as e:
        print(f"❌ Case creation error: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Salesforce Connection Test")
    print("=" * 50)

    # Test 1: Environment variables
    env_ok = test_env_variables()
    if not env_ok:
        print("\n❌ Environment setup failed. Please fix .env file first.")
        sys.exit(1)

    # Test 2: Salesforce connection
    connection_ok = test_salesforce_connection()
    if not connection_ok:
        print("\n❌ Salesforce connection failed.")
        print("Please check your credentials and network connection.")
        sys.exit(1)

    # Test 3: Case creation
    case_ok = test_case_creation()
    if not case_ok:
        print("\n❌ Case creation failed.")
        print("Please check your Salesforce permissions and custom fields.")
        sys.exit(1)

    print("\n🎉 All tests passed! Your Salesforce integration is working correctly.")
    print("You can now run the AI Helpdesk application.")

if __name__ == "__main__":
    main()
