"""
Outbound Sales Crew - Main execution script.

This script demonstrates the complete outbound sales automation workflow
using CrewAI agents to enrich leads and generate personalized email campaigns.
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv

from crew.crew import OutboundSalesCrew


def load_environment():
    """Load environment variables from .env file."""
    load_dotenv()
    
    # Verify required environment variables
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file and ensure all required variables are set.")
        return False
    
    print("✅ Environment variables loaded successfully")
    return True


def load_sample_lead():
    """Load sample lead profile from JSON file."""
    try:
        sample_file = Path("sample_data/lead_profile.json")
        with open(sample_file, 'r') as f:
            lead_profile = json.load(f)
        
        print(f"✅ Loaded lead profile for: {lead_profile.get('name', 'Unknown')}")
        return lead_profile
    
    except FileNotFoundError:
        print("❌ Sample lead profile file not found at sample_data/lead_profile.json")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing lead profile JSON: {e}")
        return None


def get_product_info():
    """Get product/service information for the outreach campaign."""
    # This would typically come from a configuration file or database
    # For this demo, we'll use a sample product
    return {
        "name": "DevOps Acceleration Platform",
        "description": "AI-powered DevOps platform that automates CI/CD pipelines, monitors deployments, and optimizes infrastructure costs",
        "benefits": [
            "Reduce deployment time by 60%",
            "Cut infrastructure costs by 30%", 
            "Improve code quality with automated testing",
            "Scale engineering teams efficiently",
            "24/7 intelligent monitoring and alerting"
        ],
        "target_outcome": "Accelerate development velocity while maintaining reliability and reducing operational overhead",
        "pricing_model": "SaaS subscription starting at $500/month",
        "use_cases": [
            "Automated CI/CD pipeline setup",
            "Infrastructure cost optimization",
            "Development team productivity improvement",
            "Enterprise-grade monitoring and observability"
        ],
        "differentiators": [
            "AI-powered optimization recommendations",
            "seamless integration with existing tools",
            "Enterprise-grade security and compliance",
            "24/7 expert support and onboarding"
        ]
    }


def display_campaign_results(campaign):
    """Display the generated campaign results in a readable format."""
    print("\n" + "="*80)
    print("🎯 OUTBOUND SALES CAMPAIGN GENERATED")
    print("="*80)
    
    # Lead summary
    lead = campaign["lead_profile"]
    print(f"\n👤 TARGET PROSPECT:")
    print(f"   Name: {lead.get('name', 'N/A')}")
    print(f"   Title: {lead.get('job_title', 'N/A')}")
    print(f"   Company: {lead.get('company', 'N/A')} ({lead.get('company_size', 'N/A')} employees)")
    print(f"   Industry: {lead.get('industry', 'N/A')}")
    
    # Campaign summary
    summary = campaign["campaign_summary"]
    print(f"\n📊 CAMPAIGN STRATEGY:")
    print(f"   Target Persona: {summary.get('target_persona', 'N/A')}")
    print(f"   Company Size: {summary.get('company_size', 'N/A')}")
    print(f"   Email Sequence: {summary.get('email_sequence_count', 0)} emails over {summary.get('total_campaign_duration', 'N/A')}")
    print(f"   Communication Style: {summary.get('communication_style', 'N/A')}")
    
    # Primary pain points
    pain_points = summary.get('primary_pain_points', [])
    if pain_points:
        print(f"\n🎯 IDENTIFIED PAIN POINTS:")
        for point in pain_points[:3]:  # Show top 3
            print(f"   • {point}")
    
    # Email sequence
    emails = campaign["emails"]
    
    print(f"\n📧 COLD EMAIL:")
    cold_email = emails["cold_email"]
    print(f"   Subject: {cold_email.get('subject', 'N/A')}")
    print(f"   Body Preview: {cold_email.get('body', 'N/A')[:100]}...")
    
    print(f"\n📬 FOLLOW-UP SEQUENCE:")
    for i, followup in enumerate(emails["followups"], 1):
        print(f"   Follow-up #{i} (Day {followup.get('send_after_days', 'N/A')}):")
        print(f"     Subject: {followup.get('subject', 'N/A')}")
        print(f"     Preview: {followup.get('body', 'N/A')[:80]}...")
    
    # Timeline
    print(f"\n📅 EXECUTION TIMELINE:")
    for item in campaign["execution_timeline"]:
        print(f"   Day {item['day']}: {item['action']} - {item['status']}")
    
    # Success metrics
    print(f"\n📈 SUCCESS METRICS TO TRACK:")
    metrics = campaign["success_metrics"]["primary_metrics"]
    for metric in metrics:
        benchmark = campaign["success_metrics"]["benchmarks"].get(f"cold_email_{metric}", "Track manually")
        print(f"   • {metric.replace('_', ' ').title()}: {benchmark}")


def save_campaign_output(campaign, output_dir="output"):
    """Save campaign output to files for easy use."""
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Save complete campaign as JSON
    campaign_file = Path(output_dir) / "complete_campaign.json"
    with open(campaign_file, 'w') as f:
        json.dump(campaign, f, indent=2, default=str)
    
    # Save individual emails as text files
    emails = campaign["emails"]
    
    # Cold email
    cold_email_file = Path(output_dir) / "cold_email.txt"
    with open(cold_email_file, 'w') as f:
        f.write(f"Subject: {emails['cold_email']['subject']}\n\n")
        f.write(emails['cold_email']['body'])
    
    # Follow-up emails
    for i, followup in enumerate(emails["followups"], 1):
        followup_file = Path(output_dir) / f"followup_{i}.txt"
        with open(followup_file, 'w') as f:
            f.write(f"Subject: {followup['subject']}\n\n")
            f.write(followup['body'])
    
    print(f"\n💾 Campaign files saved to '{output_dir}/' directory")
    print(f"   • complete_campaign.json - Full campaign data")
    print(f"   • cold_email.txt - Initial outreach email")
    print(f"   • followup_1.txt - First follow-up email")
    print(f"   • followup_2.txt - Second follow-up email")


def main():
    """Main execution function."""
    print("🚀 Starting Outbound Sales Crew")
    print("=" * 50)
    
    # Load environment variables
    if not load_environment():
        return
    
    # Load sample lead profile
    lead_profile = load_sample_lead()
    if not lead_profile:
        return
    
    # Get product information
    product_info = get_product_info()
    print(f"✅ Product info loaded: {product_info['name']}")
    
    try:
        # Initialize the crew
        print("\n🤖 Initializing Outbound Sales Crew...")
        crew = OutboundSalesCrew()
        
        # Display crew information
        crew_info = crew.get_crew_info()
        print(f"✅ {crew_info['crew_name']} v{crew_info['version']} initialized")
        print(f"   Agents: {len(crew_info['agents'])} specialized agents")
        
        # Generate the campaign
        print(f"\n🎯 Generating outbound sales campaign...")
        print(f"   Target: {lead_profile['name']} at {lead_profile['company']}")
        
        campaign = crew.run_crew_workflow(lead_profile, product_info)
        
        # Display results
        display_campaign_results(campaign)
        
        # Save output files
        save_campaign_output(campaign)
        
        print(f"\n✅ Campaign generation completed successfully!")
        print(f"🎉 Ready to launch outbound sales campaign for {lead_profile['name']}")
        
    except Exception as e:
        print(f"\n❌ Error generating campaign: {e}")
        print("Please check your API keys and try again.")
        raise


if __name__ == "__main__":
    main()
