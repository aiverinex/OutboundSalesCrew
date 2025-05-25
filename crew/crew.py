"""
Outbound Sales Crew - Main crew orchestration for automated sales outreach.
"""

from crewai import Crew, Process
from agents.research_agent import LeadResearchAgent
from agents.email_agent import EmailDraftingAgent
from agents.followup_agent import FollowUpAgent
from tasks.task import OutboundSalesTasks
import json
from datetime import datetime


class OutboundSalesCrew:
    """Main crew for orchestrating the outbound sales automation workflow."""
    
    def __init__(self):
        """Initialize the crew with all agents and tasks."""
        # Initialize agent classes
        self.research_agent_class = LeadResearchAgent()
        self.email_agent_class = EmailDraftingAgent()
        self.followup_agent_class = FollowUpAgent()
        
        # Create agent instances
        self.research_agent = self.research_agent_class.create_agent()
        self.email_agent = self.email_agent_class.create_agent()
        self.followup_agent = self.followup_agent_class.create_agent()
        
        # Initialize tasks
        self.tasks = OutboundSalesTasks()
    
    def create_outreach_campaign(self, lead_profile, product_info):
        """
        Create a complete outbound sales campaign for a lead.
        
        Args:
            lead_profile (dict): Basic lead information
            product_info (dict): Product/service information
            
        Returns:
            dict: Complete campaign with all emails and timing
        """
        
        # Step 1: Enrich lead data
        print("🔍 Enriching lead data...")
        enriched_profile = self.research_agent_class.enrich_lead_data(lead_profile)
        
        # Step 2: Generate cold email
        print("✍️ Generating personalized cold email...")
        cold_email = self.email_agent_class.generate_cold_email(enriched_profile, product_info)
        
        # Step 3: Create follow-up sequence
        print("📧 Creating follow-up sequence...")
        followup_sequence = self.followup_agent_class.generate_followup_sequence(
            enriched_profile, cold_email, product_info
        )
        
        # Step 4: Compile complete campaign
        campaign = {
            "lead_profile": enriched_profile,
            "campaign_created_at": datetime.now().isoformat(),
            "emails": {
                "cold_email": cold_email,
                "followups": followup_sequence
            },
            "campaign_summary": self._generate_campaign_summary(
                enriched_profile, cold_email, followup_sequence
            ),
            "execution_timeline": self._generate_timeline(cold_email, followup_sequence),
            "success_metrics": self._define_success_metrics(),
            "next_steps": self._generate_next_steps(enriched_profile)
        }
        
        return campaign
    
    def run_crew_workflow(self, lead_profile, product_info):
        """
        Run the full CrewAI workflow for outbound sales automation.
        
        Args:
            lead_profile (dict): Basic lead information
            product_info (dict): Product/service information
            
        Returns:
            dict: Results from the crew execution
        """
        
        # Create tasks
        research_task = self.tasks.research_lead_task(self.research_agent, lead_profile)
        
        # Note: For this implementation, we're using direct method calls instead of 
        # full CrewAI task execution to ensure reliable OpenAI integration
        # This approach maintains the CrewAI structure while ensuring production readiness
        
        return self.create_outreach_campaign(lead_profile, product_info)
    
    def _generate_campaign_summary(self, enriched_profile, cold_email, followup_sequence):
        """Generate a summary of the campaign strategy."""
        return {
            "target_persona": f"{enriched_profile.get('job_title', 'Professional')} at {enriched_profile.get('company', 'target company')}",
            "company_size": enriched_profile.get('company_size_category', 'unknown'),
            "primary_pain_points": enriched_profile.get('likely_pain_points', []),
            "personalization_approach": enriched_profile.get('personalization_hooks', []),
            "email_sequence_count": 1 + len(followup_sequence),
            "total_campaign_duration": "7 days",
            "communication_style": enriched_profile.get('role_context', {}).get('communication_style', 'professional')
        }
    
    def _generate_timeline(self, cold_email, followup_sequence):
        """Generate execution timeline for the campaign."""
        timeline = [
            {
                "day": 0,
                "action": "Send cold email",
                "email_type": "cold_email",
                "subject": cold_email.get('subject', ''),
                "status": "ready"
            }
        ]
        
        for followup in followup_sequence:
            timeline.append({
                "day": followup.get('send_after_days', 0),
                "action": f"Send {followup.get('type', 'followup')}",
                "email_type": followup.get('type', 'followup'),
                "subject": followup.get('subject', ''),
                "status": "scheduled"
            })
        
        return timeline
    
    def _define_success_metrics(self):
        """Define metrics to track campaign success."""
        return {
            "primary_metrics": [
                "open_rate",
                "reply_rate", 
                "meeting_scheduled",
                "positive_response"
            ],
            "benchmarks": {
                "cold_email_open_rate": "20-25%",
                "cold_email_reply_rate": "2-5%",
                "followup_engagement_lift": "10-15%",
                "meeting_conversion": "1-3%"
            },
            "tracking_points": [
                "Email delivered",
                "Email opened", 
                "Links clicked",
                "Reply received",
                "Meeting scheduled",
                "Opt-out requested"
            ]
        }
    
    def _generate_next_steps(self, enriched_profile):
        """Generate recommended next steps for the sales team."""
        role_level = enriched_profile.get('role_context', {}).get('level', 'Professional')
        
        next_steps = [
            "Review and customize emails before sending",
            "Set up email tracking and analytics",
            "Prepare for potential responses and objections",
            "Schedule follow-up reminders in CRM"
        ]
        
        # Add role-specific recommendations
        if role_level == "C-Level":
            next_steps.append("Prepare executive-level meeting agenda if they respond")
            next_steps.append("Research recent company announcements or funding")
        elif role_level == "Technical Leadership":
            next_steps.append("Prepare technical demo or proof of concept")
            next_steps.append("Gather relevant case studies from similar tech companies")
        
        return next_steps
    
    def get_crew_info(self):
        """Get information about the crew and its capabilities."""
        return {
            "crew_name": "Outbound Sales Crew",
            "version": "1.0.0",
            "agents": [
                {
                    "name": "Lead Research Agent",
                    "role": "Lead Research Specialist",
                    "capabilities": ["lead enrichment", "company analysis", "role context analysis"]
                },
                {
                    "name": "Email Drafting Agent", 
                    "role": "Sales Email Specialist",
                    "capabilities": ["personalized email generation", "subject line optimization", "CTA creation"]
                },
                {
                    "name": "Follow-up Agent",
                    "role": "Follow-up Communication Specialist", 
                    "capabilities": ["follow-up sequence creation", "timing optimization", "engagement strategies"]
                }
            ],
            "workflow": [
                "1. Enrich lead profile with company and role context",
                "2. Generate personalized cold outreach email", 
                "3. Create natural follow-up email sequence",
                "4. Compile complete campaign with timeline and metrics"
            ],
            "supported_integrations": ["OpenAI GPT", "Email platforms", "CRM systems"],
            "output_formats": ["JSON", "Email templates", "Campaign reports"]
        }
