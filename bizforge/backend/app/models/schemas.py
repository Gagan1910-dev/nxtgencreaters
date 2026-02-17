from pydantic import BaseModel
from typing import List, Optional

# --- Request Models ---
class BrandRequest(BaseModel):
    business_idea: str
    industry: str
    target_audience: Optional[str] = "General Public"
    tone: Optional[str] = "Professional"

# --- Response Models ---
class BrandIdentity(BaseModel):
    name: str # e.g., "EcoVibe"
    tagline: str # e.g., "Sustainably Yours."
    score: int # e.g., 95

class SocialContent(BaseModel):
    platform: str # "Instagram", "LinkedIn", "Twitter"
    content: str
    hashtags: List[str]

class BrandKit(BaseModel):
    identity: List[BrandIdentity]
    description: str
    social_media: List[SocialContent]
    email_copy: str
    logo_prompt: str # Prompt used for generation
    logo_url: str # Placeholder URL or Base64
    sentiment_analysis: str # "Positive tone detected..."
    color_palette: List[str] # Hex codes
    brand_summary: str # Elevator pitch

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = ""

class ChatResponse(BaseModel):
    response: str

# --- Strategy Analyzer Models ---
class StrategyRequest(BaseModel):
    business_idea: str

class TargetAudienceData(BaseModel):
    demographics: str
    behaviors: str
    pain_points: str
    why_choose: str

class AttractionStrategyData(BaseModel):
    messaging_style: str
    emotional_triggers: str
    trust_building: str
    content_tone: str

class MarketingStrategiesData(BaseModel):
    platforms: str
    content_strategy: str
    collaborations: str
    retention: str

class StrategyAnalysis(BaseModel):
    industry_category: str
    market_offerings: List[str]
    saturation_level: str
    saturation_explanation: str
    differentiation_opportunities: List[str]
    value_positioning: List[str]
    target_audience: TargetAudienceData
    attraction_strategy: AttractionStrategyData
    marketing_strategies: MarketingStrategiesData
    strategic_advice: str
