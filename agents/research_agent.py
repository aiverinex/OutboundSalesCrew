"""
Lead Research Agent for enriching lead data with company and role context.
"""

from crewai import Agent
from crewai_tools import SerperDevTool
import os


class LeadResearchAgent:
    """Agent responsible for enriching lead data with additional context."""
    
    def __init__(self):
        self.search_tool = SerperDevTool()
    
    def create_agent(self):
        """Create and return the lead research agent."""
        return Agent(
            role="Lead Research Specialist",
            goal="Enrich lead profiles with comprehensive company and role-specific insights for personalized outreach",
            backstory="""You are an expert B2B sales researcher with deep knowledge of 
            company structures, industry trends, and professional roles. You excel at 
            gathering relevant context about prospects and their organizations to enable 
            highly personalized outreach. Your research helps sales teams understand 
            pain points, company priorities, and the best approach for each lead.
            
            You always return your analysis in a structured JSON format that includes:
            - Enriched lead profile with additional context
            - Company size analysis and characteristics
            - Role-specific priorities and communication preferences
            - Industry insights and trends
            - Identified pain points and personalization hooks""",
            tools=[self.search_tool] if os.getenv("SERPER_API_KEY") else [],
            verbose=True,
            allow_delegation=False,
            max_iter=3
        )
    
    def enrich_lead_data(self, lead_profile):
        """
        Enrich lead data with additional context about company and role.
        
        Args:
            lead_profile (dict): Basic lead information
            
        Returns:
            dict: Enriched lead profile with additional context
        """
        # Extract basic information
        company = lead_profile.get('company', '')
        job_title = lead_profile.get('job_title', '')
        industry = lead_profile.get('industry', '')
        
        # Determine company size category
        company_size = lead_profile.get('company_size', 0)
        if company_size < 50:
            size_category = "small startup"
            pain_points = ["scaling challenges", "resource constraints", "process optimization"]
        elif company_size < 500:
            size_category = "mid-size company"
            pain_points = ["operational efficiency", "team coordination", "growth management"]
        else:
            size_category = "enterprise organization"
            pain_points = ["system integration", "compliance requirements", "enterprise scalability"]
        
        # Analyze role-specific context
        role_context = self._analyze_role_context(job_title)
        
        # Industry-specific insights
        industry_insights = self._get_industry_insights(industry)
        
        # Create enriched profile
        enriched_profile = {
            **lead_profile,
            "company_size_category": size_category,
            "likely_pain_points": pain_points,
            "role_context": role_context,
            "industry_insights": industry_insights,
            "personalization_hooks": self._generate_personalization_hooks(
                company, job_title, industry, size_category
            )
        }
        
        return enriched_profile
    
    def _analyze_role_context(self, job_title):
        """Analyze job title to understand role responsibilities and priorities."""
        title_lower = job_title.lower()
        
        if any(word in title_lower for word in ['ceo', 'founder', 'president']):
            return {
                "level": "C-Level",
                "priorities": ["company growth", "strategic decisions", "revenue optimization"],
                "communication_style": "high-level, results-focused"
            }
        elif any(word in title_lower for word in ['cto', 'vp engineering', 'head of tech']):
            return {
                "level": "Technical Leadership",
                "priorities": ["technical innovation", "team productivity", "system reliability"],
                "communication_style": "technical depth, solution-oriented"
            }
        elif any(word in title_lower for word in ['cmo', 'marketing director', 'head of marketing']):
            return {
                "level": "Marketing Leadership",
                "priorities": ["lead generation", "brand growth", "marketing ROI"],
                "communication_style": "metrics-driven, creative solutions"
            }
        elif any(word in title_lower for word in ['sales director', 'vp sales', 'head of sales']):
            return {
                "level": "Sales Leadership",
                "priorities": ["revenue growth", "sales efficiency", "team performance"],
                "communication_style": "results-focused, competitive advantage"
            }
        elif any(word in title_lower for word in ['hr', 'people', 'talent']):
            return {
                "level": "Human Resources",
                "priorities": ["employee experience", "talent retention", "organizational culture"],
                "communication_style": "people-first, collaborative approach"
            }
        else:
            return {
                "level": "Professional",
                "priorities": ["operational efficiency", "process improvement", "professional growth"],
                "communication_style": "practical solutions, clear benefits"
            }
    
    def _get_industry_insights(self, industry):
        """Get industry-specific insights and trends."""
        industry_lower = industry.lower()
        
        if 'technology' in industry_lower or 'software' in industry_lower:
            return {
                "key_trends": ["AI adoption", "cloud migration", "cybersecurity"],
                "common_challenges": ["scaling infrastructure", "talent acquisition", "rapid innovation"]
            }
        elif 'healthcare' in industry_lower or 'medical' in industry_lower:
            return {
                "key_trends": ["digital transformation", "patient experience", "regulatory compliance"],
                "common_challenges": ["data security", "cost management", "regulatory changes"]
            }
        elif 'finance' in industry_lower or 'banking' in industry_lower:
            return {
                "key_trends": ["fintech disruption", "regulatory compliance", "digital banking"],
                "common_challenges": ["legacy system modernization", "regulatory compliance", "customer experience"]
            }
        elif 'retail' in industry_lower or 'ecommerce' in industry_lower:
            return {
                "key_trends": ["omnichannel experience", "personalization", "supply chain optimization"],
                "common_challenges": ["inventory management", "customer acquisition", "digital transformation"]
            }
        else:
            return {
                "key_trends": ["digital transformation", "operational efficiency", "customer experience"],
                "common_challenges": ["process optimization", "technology adoption", "competitive pressure"]
            }
    
    def _generate_personalization_hooks(self, company, job_title, industry, size_category):
        """Generate specific personalization hooks for outreach."""
        hooks = []
        
        # Company-specific hook
        hooks.append(f"Given {company}'s position as a {size_category} in the {industry} space")
        
        # Role-specific hook
        role_context = self._analyze_role_context(job_title)
        hooks.append(f"As a {role_context['level']} professional focused on {', '.join(role_context['priorities'][:2])}")
        
        # Industry hook
        industry_insights = self._get_industry_insights(industry)
        hooks.append(f"With the current {industry} trends around {', '.join(industry_insights['key_trends'][:2])}")
        
        return hooks
