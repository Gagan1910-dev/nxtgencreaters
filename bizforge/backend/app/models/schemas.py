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
