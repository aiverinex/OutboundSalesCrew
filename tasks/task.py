"""
Tasks for the Outbound Sales Crew workflow.
"""

from crewai import Task
from textwrap import dedent


class OutboundSalesTasks:
    """Task definitions for the outbound sales automation workflow."""
    
    def research_lead_task(self, agent, lead_profile):
        """Task for researching and enriching lead data."""
        return Task(
            description=dedent(f"""
                Analyze and enrich the following lead profile with comprehensive 
                company and role-specific insights:
                
                Lead Profile: {lead_profile}
                
                Your research should include:
                1. Company context and size analysis
                2. Industry-specific insights and trends
                3. Role responsibilities and priorities based on job title
                4. Likely pain points and challenges
                5. Personalization hooks for outreach
                6. Communication style preferences for this role level
                
                Provide a detailed enriched profile that will enable highly 
                personalized and relevant outreach.
            """),
            agent=agent,
            expected_output="""A comprehensive enriched lead profile containing:
            - Original lead data plus additional context
            - Company size category and characteristics
            - Role-specific priorities and communication preferences
            - Industry insights and current trends
            - Identified pain points and challenges
            - Specific personalization hooks for outreach
            - Recommended approach strategy""",
            async_execution=False
        )
    
    def draft_cold_email_task(self, agent, enriched_profile, product_info):
        """Task for drafting the initial cold outreach email."""
        return Task(
            description=dedent(f"""
                Create a compelling, personalized cold outreach email using the 
                enriched lead profile and product information.
                
                Enriched Lead Profile: {enriched_profile}
                Product Information: {product_info}
                
                The email should:
                1. Use specific personalization from the enriched profile
                2. Address the prospect's likely challenges and priorities
                3. Clearly communicate value proposition relevant to their role
                4. Include social proof or credibility indicators
                5. Have an engaging subject line that encourages opening
                6. End with a clear, low-pressure call-to-action
                7. Be conversational and human (150-200 words max)
                8. Avoid generic templates or corporate speak
                
                Focus on building genuine connection and demonstrating understanding 
                of their specific situation.
            """),
            agent=agent,
            expected_output="""A complete cold email package including:
            - Compelling subject line that encourages opens
            - Personalized email body (150-200 words)
            - Clear value proposition tied to prospect's challenges
            - Specific personalization elements from research
            - Professional but conversational tone
            - Strong call-to-action that's easy to respond to""",
            async_execution=False
        )
    
    def create_followup_sequence_task(self, agent, enriched_profile, cold_email, product_info):
        """Task for creating the follow-up email sequence."""
        return Task(
            description=dedent(f"""
                Create a sequence of natural, value-added follow-up emails for 
                prospects who haven't responded to the initial outreach.
                
                Enriched Lead Profile: {enriched_profile}
                Original Cold Email: {cold_email}
                Product Information: {product_info}
                
                Create 2 follow-up emails:
                1. First follow-up (3 days after initial email):
                   - Add new value or insight not covered in original email
                   - Reference original email without being repetitive
                   - Maintain helpful, resource-focused tone
                   - 100-150 words maximum
                
                2. Second follow-up (7 days after initial email):
                   - Take a different angle or approach
                   - Perhaps ask for feedback or offer alternative value
                   - Show understanding if they're not interested
                   - Include graceful opt-out option
                   - 100-150 words maximum
                
                Each follow-up should feel natural and helpful rather than pushy,
                with different subject lines and fresh content.
            """),
            agent=agent,
            expected_output="""A complete follow-up sequence containing:
            - Follow-up #1 (3-day): Subject line and body with new value/insight
            - Follow-up #2 (7-day): Subject line and body with different angle
            - Timing recommendations for each follow-up
            - Clear opt-out options in each message
            - Natural, helpful tone throughout sequence
            - No repetition of original email content""",
            async_execution=False
        )
    
    def compile_outreach_campaign_task(self, agent, research_result, cold_email, followup_sequence):
        """Task for compiling the complete outreach campaign."""
        return Task(
            description=dedent(f"""
                Compile all components into a complete, ready-to-execute outbound 
                sales campaign for this lead.
                
                Components to compile:
                - Research insights: {research_result}
                - Cold email: {cold_email}
                - Follow-up sequence: {followup_sequence}
                
                Create a comprehensive campaign package that includes:
                1. Executive summary of the lead and approach strategy
                2. Complete email sequence with timing recommendations
                3. Key personalization elements used
                4. Suggested next steps for manual review
                5. Success metrics to track
                6. Alternative approaches if initial sequence doesn't work
                
                Format the output for easy use by sales teams.
            """),
            agent=agent,
            expected_output="""A complete outbound sales campaign package including:
            - Lead profile summary and key insights
            - Full email sequence (initial + 2 follow-ups) with timing
            - Personalization strategy and key elements used
            - Recommended tracking metrics and success indicators
            - Formatted templates ready for sales team execution
            - Alternative approach suggestions for continued outreach""",
            async_execution=False
        )
