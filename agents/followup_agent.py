"""
Follow-up Agent for creating natural, friendly follow-up messages for non-responders.
"""

from crewai import Agent
import json
import os
from openai import OpenAI
from datetime import datetime, timedelta


class FollowUpAgent:
    """Agent responsible for creating follow-up email sequences."""
    
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"
    
    def create_agent(self):
        """Create and return the follow-up agent."""
        return Agent(
            role="Follow-up Communication Specialist",
            goal="Create natural, non-pushy follow-up messages that re-engage prospects without being annoying",
            backstory="""You are a relationship-building expert who understands the delicate 
            art of following up with busy professionals. You know that persistence pays off, 
            but only when done with finesse and genuine value. Your follow-ups feel natural 
            and helpful rather than salesy or desperate. You're skilled at finding new angles, 
            adding fresh value, and making it easy for prospects to engage when they're ready. 
            Your messages are brief, friendly, and always give the recipient an easy way out.""",
            verbose=True,
            allow_delegation=False,
            max_iter=2
        )
    
    def generate_followup_sequence(self, enriched_lead_profile, original_email, product_info):
        """
        Generate a sequence of follow-up messages.
        
        Args:
            enriched_lead_profile (dict): Enriched lead information
            original_email (dict): The original cold email sent
            product_info (dict): Information about the product/service
            
        Returns:
            list: List of follow-up emails with timing
        """
        followups = []
        
        # Generate first follow-up (3 days after initial email)
        followup_1 = self._generate_single_followup(
            enriched_lead_profile, 
            original_email, 
            product_info, 
            followup_number=1,
            days_after=3
        )
        followups.append(followup_1)
        
        # Generate second follow-up (7 days after initial email)
        followup_2 = self._generate_single_followup(
            enriched_lead_profile, 
            original_email, 
            product_info, 
            followup_number=2,
            days_after=7
        )
        followups.append(followup_2)
        
        return followups
    
    def _generate_single_followup(self, lead_profile, original_email, product_info, followup_number, days_after):
        """Generate a single follow-up email."""
        
        prompt = self._build_followup_prompt(
            lead_profile, 
            original_email, 
            product_info, 
            followup_number,
            days_after
        )
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert at writing natural, non-pushy follow-up emails 
                        that re-engage prospects. Your follow-ups are brief (100-150 words), add new value 
                        or perspective, and feel genuinely helpful rather than sales-driven. Always include 
                        an easy opt-out and keep the tone friendly and professional. Return your response 
                        in JSON format with 'subject' and 'body' fields."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.8
            )
            
            content = response.choices[0].message.content
            if content:
                result = json.loads(content)
            else:
                raise Exception("Empty response from OpenAI")
            
            # Calculate send date
            send_date = datetime.now() + timedelta(days=days_after)
            
            return {
                "type": f"followup_{followup_number}",
                "subject": result.get("subject", ""),
                "body": result.get("body", ""),
                "send_after_days": days_after,
                "suggested_send_date": send_date.isoformat(),
                "generated_at": self._get_timestamp()
            }
            
        except Exception as e:
            raise Exception(f"Failed to generate follow-up {followup_number}: {e}")
    
    def _build_followup_prompt(self, lead_profile, original_email, product_info, followup_number, days_after):
        """Build the prompt for follow-up generation."""
        
        # Extract key information
        name = lead_profile.get('name', 'there')
        company = lead_profile.get('company', '')
        job_title = lead_profile.get('job_title', '')
        industry_insights = lead_profile.get('industry_insights', {})
        
        # Different approaches for different follow-ups
        if followup_number == 1:
            approach = "Add a new piece of value, insight, or resource that wasn't in the original email"
            tone = "Helpful and resource-focused"
        else:
            approach = "Take a different angle, perhaps asking for feedback or offering to connect them with someone else"
            tone = "Gracefully persistent but understanding"
        
        prompt = f"""
        Write follow-up email #{followup_number} (to be sent {days_after} days after the original email):
        
        PROSPECT DETAILS:
        - Name: {name}
        - Job Title: {job_title}
        - Company: {company}
        - Industry Trends: {', '.join(industry_insights.get('key_trends', []))}
        
        ORIGINAL EMAIL CONTEXT:
        - Subject: {original_email.get('subject', '')}
        - Main value proposition from original email
        
        PRODUCT/SERVICE:
        - Name: {product_info.get('name', 'our solution')}
        - Key Benefits: {', '.join(product_info.get('benefits', []))}
        
        FOLLOW-UP REQUIREMENTS:
        1. Approach: {approach}
        2. Tone: {tone}
        3. Reference the original email briefly without being repetitive
        4. Add NEW value (insight, resource, different perspective)
        5. Keep it short and scannable (100-150 words max)
        6. Include a soft call-to-action
        7. Always provide an easy opt-out option
        8. Subject line should be different from the original
        
        FOLLOW-UP STRATEGIES TO CONSIDER:
        - Share a relevant industry insight or trend
        - Offer a useful resource (guide, template, case study)
        - Ask for their perspective on an industry challenge
        - Mention a mutual connection or similar company success
        - Provide a specific, small commitment (5-minute call, quick question)
        
        Return as JSON with 'subject' and 'body' fields.
        """
        
        return prompt.strip()
    
    def _get_timestamp(self):
        """Get current timestamp for tracking."""
        return datetime.now().isoformat()
