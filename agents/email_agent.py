"""
Email Drafting Agent for creating personalized cold outreach emails using OpenAI GPT.
"""

from crewai import Agent
import json
import os
from openai import OpenAI


class EmailDraftingAgent:
    """Agent responsible for creating personalized sales emails."""
    
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"
    
    def create_agent(self):
        """Create and return the email drafting agent."""
        return Agent(
            role="Sales Email Specialist",
            goal="Create compelling, personalized cold outreach emails using OpenAI that drive engagement and responses",
            backstory="""You are a master of B2B sales communication with years of experience 
            crafting emails that get opened, read, and responded to. You understand the psychology 
            of decision-makers and know how to present value propositions in a way that resonates 
            with busy professionals. Your emails are conversational, benefit-focused, and always 
            include clear calls-to-action. You avoid generic templates and instead create authentic, 
            human-sounding messages that build genuine connections.
            
            You use OpenAI to generate personalized content and always return emails in JSON format
            with 'subject' and 'body' fields, ensuring 150-200 word length and professional tone.""",
            verbose=True,
            allow_delegation=False,
            max_iter=2
        )
    
    def generate_cold_email(self, enriched_lead_profile, product_info):
        """
        Generate a personalized cold outreach email.
        
        Args:
            enriched_lead_profile (dict): Enriched lead information
            product_info (dict): Information about the product/service being sold
            
        Returns:
            dict: Generated email with subject and body
        """
        prompt = self._build_email_prompt(enriched_lead_profile, product_info, "cold_email")
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert B2B sales email writer. Create personalized, 
                        engaging cold outreach emails that feel authentic and human. Focus on the 
                        prospect's specific challenges and how your solution can help. Keep emails 
                        concise (150-200 words), conversational, and always include a clear, 
                        low-pressure call-to-action. Return your response in JSON format with 
                        'subject' and 'body' fields."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            if content:
                result = json.loads(content)
            else:
                raise Exception("Empty response from OpenAI")
            return {
                "type": "cold_email",
                "subject": result.get("subject", ""),
                "body": result.get("body", ""),
                "generated_at": self._get_timestamp()
            }
            
        except Exception as e:
            raise Exception(f"Failed to generate cold email: {e}")
    
    def _build_email_prompt(self, lead_profile, product_info, email_type):
        """Build the prompt for email generation."""
        
        # Extract key information
        name = lead_profile.get('name', 'there')
        company = lead_profile.get('company', '')
        job_title = lead_profile.get('job_title', '')
        role_context = lead_profile.get('role_context', {})
        pain_points = lead_profile.get('likely_pain_points', [])
        personalization_hooks = lead_profile.get('personalization_hooks', [])
        
        prompt = f"""
        Write a personalized {email_type.replace('_', ' ')} for this prospect:
        
        PROSPECT DETAILS:
        - Name: {name}
        - Job Title: {job_title}
        - Company: {company}
        - Role Level: {role_context.get('level', 'Professional')}
        - Key Priorities: {', '.join(role_context.get('priorities', []))}
        - Likely Pain Points: {', '.join(pain_points)}
        
        PERSONALIZATION HOOKS:
        {chr(10).join(f'- {hook}' for hook in personalization_hooks)}
        
        PRODUCT/SERVICE INFORMATION:
        - Name: {product_info.get('name', 'our solution')}
        - Description: {product_info.get('description', 'a comprehensive business solution')}
        - Key Benefits: {', '.join(product_info.get('benefits', ['improved efficiency', 'cost savings']))}
        - Target Outcome: {product_info.get('target_outcome', 'business growth and optimization')}
        
        EMAIL REQUIREMENTS:
        1. Use the prospect's name and reference their specific role/company
        2. Connect their likely challenges to your solution's benefits
        3. Keep it conversational and human (avoid corporate speak)
        4. Include social proof or credibility indicators if relevant
        5. End with a soft, low-pressure call-to-action
        6. Subject line should be intriguing but not salesy
        7. Total length: 150-200 words maximum
        
        Return as JSON with 'subject' and 'body' fields.
        """
        
        return prompt.strip()
    
    def _get_timestamp(self):
        """Get current timestamp for tracking."""
        from datetime import datetime
        return datetime.now().isoformat()
