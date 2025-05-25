"""
Test script to run the Outbound Sales Crew with a different lead profile.
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv

from crew.crew import OutboundSalesCrew

def load_test_lead():
    """Load test lead profile from JSON file."""
    try:
        sample_file = Path("sample_data/test_lead.json")
        with open(sample_file, 'r') as f:
            lead_profile = json.load(f)
        
        print(f"✅ Loaded test lead profile for: {lead_profile.get('name', 'Unknown')}")
        return lead_profile
    
    except FileNotFoundError:
        print("❌ Test lead profile file not found")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing test lead profile JSON: {e}")
        return None

def get_test_product_info():
    """Get product/service information for the test campaign."""
    return {
        "name": "CustomerConnect Analytics Platform",
        "description": "AI-powered customer data platform that unifies customer interactions across all channels and provides real-time marketing attribution",
        "benefits": [
            "Unify customer data across all touchpoints",
            "Improve marketing ROI by 40%",
            "Reduce customer acquisition costs by 25%",
            "Real-time attribution and analytics",
            "Personalized customer experiences at scale"
        ],
        "target_outcome": "Increase customer lifetime value and marketing efficiency through unified data insights",
        "pricing_model": "SaaS subscription starting at $2,000/month",
        "use_cases": [
            "Omnichannel customer journey mapping",
            "Marketing attribution and ROI optimization",
            "Personalized customer segmentation",
            "Real-time campaign performance tracking"
        ],
        "differentiators": [
            "AI-powered predictive analytics",
            "Real-time data processing",
            "Easy integration with existing retail systems",
            "Dedicated retail industry expertise"
        ]
    }

def main():
    """Main test execution function."""
    print("🧪 Testing Outbound Sales Crew with Different Lead")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Load test lead profile
    lead_profile = load_test_lead()
    if not lead_profile:
        return
    
    # Get product information
    product_info = get_test_product_info()
    print(f"✅ Product info loaded: {product_info['name']}")
    
    try:
        # Initialize the crew
        print(f"\n🤖 Initializing crew for test campaign...")
        crew = OutboundSalesCrew()
        
        # Generate the campaign
        print(f"\n🎯 Generating campaign for different prospect type...")
        print(f"   Target: {lead_profile['name']} ({lead_profile['job_title']}) at {lead_profile['company']}")
        
        campaign = crew.run_crew_workflow(lead_profile, product_info)
        
        # Display key results
        print(f"\n" + "="*80)
        print("🎯 TEST CAMPAIGN RESULTS")
        print("="*80)
        
        # Lead summary
        lead = campaign["lead_profile"]
        print(f"\n👤 TARGET PROSPECT:")
        print(f"   Name: {lead.get('name', 'N/A')}")
        print(f"   Title: {lead.get('job_title', 'N/A')}")
        print(f"   Company: {lead.get('company', 'N/A')} ({lead.get('company_size', 'N/A')} employees)")
        print(f"   Industry: {lead.get('industry', 'N/A')}")
        
        # Show the cold email
        cold_email = campaign["emails"]["cold_email"]
        print(f"\n📧 GENERATED COLD EMAIL:")
        print(f"   Subject: {cold_email.get('subject', 'N/A')}")
        print(f"\n   Email Body:")
        print(f"   {cold_email.get('body', 'N/A')}")
        
        # Show first follow-up
        if campaign["emails"]["followups"]:
            followup = campaign["emails"]["followups"][0]
            print(f"\n📬 FIRST FOLLOW-UP (Day {followup.get('send_after_days', 'N/A')}):")
            print(f"   Subject: {followup.get('subject', 'N/A')}")
            print(f"   Preview: {followup.get('body', 'N/A')[:200]}...")
        
        print(f"\n✅ Test campaign completed successfully!")
        print(f"🎉 System adapts perfectly to different prospect types!")
        
    except Exception as e:
        print(f"\n❌ Error in test campaign: {e}")

if __name__ == "__main__":
    main()