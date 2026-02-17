import httpx
import json
from app.core.config import settings
from app.models.schemas import StrategyAnalysis, TargetAudienceData, AttractionStrategyData, MarketingStrategiesData

class StrategyService:
    async def analyze_strategy(self, business_idea: str) -> StrategyAnalysis:
        """
        Generate comprehensive startup strategy analysis using AI.
        Returns structured insights across 9 key strategic areas.
        """
        if not settings.GROQ_API_KEY:
            return self._mock_strategy_analysis(business_idea)

        prompt = f"""You are a senior startup strategist, brand positioning expert, and growth marketing consultant with decades of experience guiding new businesses to stand out in competitive markets.

Analyze the business idea and provide strategic insights to help the brand differentiate, identify its ideal audience, and apply effective marketing strategies.

IMPORTANT:
Base insights on common industry patterns, market behavior, and consumer trends — do NOT reference specific company names.

==================================================
BUSINESS IDEA:
{business_idea}

==================================================
OUTPUT STRUCTURE (STRICT FORMAT)
==================================================

You MUST return ONLY a valid JSON object with the following structure. Do not include any markdown code blocks, explanations, or additional text:

{{
  "industry_category": "Primary industry and sub-category",
  "market_offerings": ["Feature 1", "Feature 2", "Feature 3"],
  "saturation_level": "LOW or MODERATE or HIGH",
  "saturation_explanation": "One-line explanation of saturation level",
  "differentiation_opportunities": [
    "Opportunity 1 focusing on unmet needs",
    "Opportunity 2 focusing on underserved groups",
    "Opportunity 3 focusing on emerging trends"
  ],
  "value_positioning": [
    "Positioning idea 1",
    "Positioning idea 2"
  ],
  "target_audience": {{
    "demographics": "Age, location, income level, etc.",
    "behaviors": "Lifestyle traits and behavior patterns",
    "pain_points": "Specific problems they face",
    "why_choose": "Why they would choose this brand"
  }},
  "attraction_strategy": {{
    "messaging_style": "Recommended messaging approach",
    "emotional_triggers": "Key emotional appeals to use",
    "trust_building": "How to build credibility",
    "content_tone": "Recommended tone and voice"
  }},
  "marketing_strategies": {{
    "platforms": "Best social media and marketing channels",
    "content_strategy": "Content types and themes to create",
    "collaborations": "Influencer and partnership opportunities",
    "retention": "Customer loyalty and retention tactics"
  }},
  "strategic_advice": "Concise expert guidance to avoid being generic and build a strong brand identity"
}}

==================================================
QUALITY RULES
==================================================

• Be precise and realistic
• Avoid generic advice
• Focus on actionable insights
• Provide strategic clarity
• Keep output structured and professional
• Return ONLY the JSON object, no markdown formatting
"""

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
                    json={
                        "model": settings.GROQ_MODEL,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7,
                        "max_tokens": 2000
                    },
                    timeout=60.0
                )
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                # Clean content if it has markdown ticks
                content = content.replace("```json", "").replace("```", "").strip()
                
                # Parse JSON response
                parsed = json.loads(content)
                
                # Convert to StrategyAnalysis model
                return StrategyAnalysis(
                    industry_category=parsed["industry_category"],
                    market_offerings=parsed["market_offerings"],
                    saturation_level=parsed["saturation_level"],
                    saturation_explanation=parsed["saturation_explanation"],
                    differentiation_opportunities=parsed["differentiation_opportunities"],
                    value_positioning=parsed["value_positioning"],
                    target_audience=TargetAudienceData(**parsed["target_audience"]),
                    attraction_strategy=AttractionStrategyData(**parsed["attraction_strategy"]),
                    marketing_strategies=MarketingStrategiesData(**parsed["marketing_strategies"]),
                    strategic_advice=parsed["strategic_advice"]
                )

        except Exception as e:
            print(f"Strategy Service Error: {e}")
            return self._mock_strategy_analysis(business_idea)

    def _mock_strategy_analysis(self, business_idea: str) -> StrategyAnalysis:
        """Fallback mock data when API is unavailable"""
        return StrategyAnalysis(
            industry_category="Technology / SaaS",
            market_offerings=[
                "Cloud-based solutions",
                "Mobile applications",
                "Analytics dashboards"
            ],
            saturation_level="MODERATE",
            saturation_explanation="Growing market with established players but room for innovation",
            differentiation_opportunities=[
                "Focus on underserved niche markets",
                "Leverage emerging AI technologies",
                "Provide superior customer experience"
            ],
            value_positioning=[
                "The most user-friendly solution in the market",
                "Affordable premium quality for small businesses"
            ],
            target_audience=TargetAudienceData(
                demographics="Ages 25-45, urban professionals, middle to upper income",
                behaviors="Tech-savvy, value efficiency, prefer digital solutions",
                pain_points="Time constraints, complex existing solutions, high costs",
                why_choose="Simplicity, affordability, and modern design"
            ),
            attraction_strategy=AttractionStrategyData(
                messaging_style="Clear, benefit-focused, and empowering",
                emotional_triggers="Time savings, stress reduction, professional growth",
                trust_building="Customer testimonials, free trials, transparent pricing",
                content_tone="Professional yet approachable, educational"
            ),
            marketing_strategies=MarketingStrategiesData(
                platforms="LinkedIn, Instagram, Product Hunt, industry forums",
                content_strategy="How-to guides, case studies, product demos, behind-the-scenes",
                collaborations="Industry micro-influencers, complementary SaaS tools",
                retention="Loyalty programs, regular feature updates, community building"
            ),
            strategic_advice="Focus on solving one specific problem exceptionally well before expanding. Build a strong community around your product and let customer success drive your marketing."
        )

strategy_service = StrategyService()
