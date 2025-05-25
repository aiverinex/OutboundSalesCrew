# Outbound Sales Crew

An intelligent, automated outbound sales system built with CrewAI that enriches lead data and generates personalized email campaigns using OpenAI GPT.

## 🎯 Overview

The Outbound Sales Crew automates the entire outbound sales process by:

- **Enriching lead data** using job title and company information
- **Writing personalized cold outreach emails** with OpenAI GPT
- **Generating natural follow-up messages** spaced over time (3-day and 7-day intervals)
- **Creating complete campaign strategies** with timing and success metrics

This system is built for the CrewAI Marketplace and follows production-ready standards with real API integrations.

## 🏗️ Architecture

### Agents
- **LeadResearchAgent**: Enriches job title + company with contextual insights
- **EmailDraftingAgent**: Creates personalized sales emails using GPT-4o
- **FollowUpAgent**: Generates natural, friendly follow-ups for non-responders

### Workflow
1. Parse lead profile from sample data
2. Enrich using company/title analysis and industry insights
3. Generate personalized cold email with OpenAI
4. Create follow-up sequence (3-day and 7-day follow-ups)
5. Compile complete campaign with execution timeline

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd outbound-sales-crew
   ```

2. **Install dependencies**
   ```bash
   pip install crewai openai python-dotenv pyyaml
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```bash
   OPENAI_API_KEY=your-openai-api-key-here
   ```

4. **Run the system**
   ```bash
   python main.py
   ```

## 📊 Sample Input/Output

### Input (Lead Profile)
```json
{
  "name": "Sarah Chen",
  "job_title": "VP of Engineering", 
  "company": "TechInnovate Solutions",
  "company_size": 150,
  "industry": "Technology"
}
```

### Output (Generated Campaign)

**Cold Email:**
```
Subject: Boosting TechInnovate's Efficiency with AI-Powered DevOps

Hi Sarah,

I hope this message finds you well. As the VP of Engineering at TechInnovate Solutions, I imagine you're constantly exploring ways to enhance operational efficiency and streamline team coordination, especially with the rapid adoption of AI and cloud technologies.

I wanted to introduce you to our DevOps Acceleration Platform, designed specifically for tech-driven companies like yours. Our AI-powered solution automates CI/CD pipelines, which has helped companies reduce deployment times by 60% and cut infrastructure costs by 30%. This could be a game-changer for your team, allowing you to focus more on innovation while we handle the nitty-gritty of deployment and monitoring.

Many mid-size tech companies have already seen significant improvements in their development velocity without sacrificing reliability, and I believe TechInnovate Solutions could experience similar benefits.

Would you be open to a brief chat? I'd love to learn more about your current challenges and explore how we might support your goals.

Looking forward to your thoughts.

Best,
[Your Name]
```

**Follow-up #1 (Day 3):**
```
Subject: Exploring AI's Role in Streamlining DevOps

Hi Sarah,

I hope this finds you well! I wanted to follow up on my previous email about our DevOps Acceleration Platform. Given your interest in AI adoption, I thought you might find this recent case study insightful: it showcases how a company similar to TechInnovate reduced deployment times by over 60% using AI-driven strategies.

I'm curious to hear your thoughts on AI's role in streamlining DevOps processes. Do you see similar opportunities or challenges in your current setup?

If you'd like to delve deeper, I'd be happy to arrange a brief chat at your convenience.

Please let me know if you prefer not to receive these emails.

Warm regards,
[Your Name]
```

**Campaign Timeline:**
- Day 0: Send cold email
- Day 3: Send follow-up #1  
- Day 7: Send follow-up #2

**Success Metrics:**
- Open Rate: 20-25%
- Reply Rate: 2-5%
- Meeting Conversion: 1-3%
