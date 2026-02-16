from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.schemas import BrandRequest, BrandKit
from app.services.branding_service import branding_service
from app.services.content_service import content_service
from app.services.visual_service import visual_service
from app.services.analysis_service import analysis_service
import asyncio

router = APIRouter()

@router.post("/generate", response_model=BrandKit)
async def generate_brand_kit(request: BrandRequest):
    try:
        # Run services in parallel where possible
        # 1. Generate identity first (need name for others)
        identities = await branding_service.generate_brand_identity(
            request.business_idea, 
            request.industry, 
            request.tone
        )
        
        selected_identity = identities[0] # Pick the first one for the full kit generation
        name = selected_identity.name

        # 2. Run other services concurrently using the generated name
        # Generate palette first to use in logo
        palette = await visual_service.generate_color_palette(request.tone)
        
        tags, logo_data, sentiment, summary = await asyncio.gather(
            content_service.generate_social_content(request.business_idea, name),
            visual_service.generate_logo(name, request.industry, request.tone, palette),
            analysis_service.analyze_sentiment(request.business_idea),
            analysis_service.summarize_description(request.business_idea)
        )
        
        email = await content_service.generate_email(name, request.business_idea)

        return BrandKit(
            identity=identities,
            description=f"A revolutionary {request.industry} startup focusing on {request.business_idea}.",
            social_media=tags,
            email_copy=email,
            logo_prompt=logo_data["prompt"],
            logo_url=logo_data["url"],
            sentiment_analysis=sentiment,
            color_palette=palette,
            brand_summary=summary
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class RegenerateLogoRequest(BaseModel):
    name: str
    industry: str
    tone: str
    color_palette: list[str]

@router.post("/regenerate-logo")
async def regenerate_logo(request: RegenerateLogoRequest):
    """Regenerate logo without regenerating entire brand kit."""
    try:
        logo_data = await visual_service.generate_logo(
            request.name,
            request.industry,
            request.tone,
            request.color_palette
        )
        return {"logo_url": logo_data["url"], "logo_prompt": logo_data["prompt"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
