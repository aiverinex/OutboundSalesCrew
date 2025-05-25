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
