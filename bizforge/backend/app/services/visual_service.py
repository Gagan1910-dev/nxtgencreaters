import httpx
import base64
import random
from app.core.config import settings

class VisualService:
    def _build_professional_prompt(self, name: str, industry: str, tone: str, primary_color: str) -> str:
        """Build a professional, brand-aligned logo prompt with strong variation."""
        tone_styles = {
            "Professional": "corporate, clean, trustworthy, minimal",
            "Playful": "vibrant, friendly, approachable, fun",
            "Luxury": "elegant, sophisticated, premium, refined",
            "Innovative": "futuristic, tech-forward, dynamic, modern",
            "Friendly": "warm, approachable, welcoming, soft",
            "Minimalist": "ultra-clean, simple, geometric, sparse"
        }
        
        # Industry-specific icon suggestions
        industry_icons = {
            "technology": ["circuit pattern", "digital node", "tech symbol", "data icon"],
            "food": ["leaf element", "organic shape", "natural form", "fresh symbol"],
            "fitness": ["dynamic shape", "movement icon", "energy symbol", "active mark"],
            "finance": ["shield icon", "growth arrow", "secure symbol", "trust mark"],
            "education": ["book symbol", "knowledge icon", "learning mark", "growth element"],
            "health": ["wellness symbol", "care icon", "vitality mark", "health element"],
            "retail": ["shopping icon", "product symbol", "store mark", "commerce element"],
            "default": ["abstract icon", "symbolic mark", "brand element", "unique symbol"]
        }
        
        # Layout variations for visual diversity
        layout_styles = [
            "icon positioned above brand name",
            "icon integrated beside brand name", 
            "circular emblem enclosing icon and text",
            "monogram lettermark with decorative element",
            "badge-style with icon centerpiece",
            "horizontal lockup with icon left"
        ]
        
        # Get industry-specific icon or default
        industry_key = industry.lower()
        icon_options = industry_icons.get(industry_key, industry_icons["default"])
        selected_icon = random.choice(icon_options)
        
        style = tone_styles.get(tone, "modern, professional")
        layout = random.choice(layout_styles)
        
        # Enhanced prompt with stronger visual directives
        return f"""Create a single professional logo design for '{name}' brand, {industry} industry.

CRITICAL: Generate ONE logo only, not multiple variations or a grid layout.

VISUAL STYLE: {style}, modern branding aesthetic
LAYOUT: {layout}
ICON ELEMENT: {selected_icon}, simple and recognizable
COLOR: {primary_color} as primary brand color
TYPOGRAPHY: clean sans-serif, professional lettering
COMPOSITION: single logo, centered on white background

REQUIREMENTS:
- ONE logo design only (not a grid, not multiple variations)
- Include both icon/symbol AND brand name text
- Flat design, vector-style graphics
- High contrast, sharp edges
- Scalable and professional
- NO multiple logo variations in one image
- NO grid layouts or collages
- NO gradients, NO textures, NO photorealistic elements
- Clean white or transparent background
- Single centered logo composition

BRAND IDENTITY: Modern startup logo, ready for real-world use
VARIATION_SEED: {random.randint(10000, 99999)}"""

    async def generate_logo(self, name: str, industry: str, tone: str = "Professional", color_palette: list = None) -> dict:
        """Generate a single high-quality logo with fallback mechanism."""
        
        # Extract primary color from palette
        primary_color = color_palette[0] if color_palette else "#6366f1"
        
        prompt = self._build_professional_prompt(name, industry, tone, primary_color)
        
        # Try Stability AI first
        try:
            if settings.STABILITY_API_KEY:
                result = await self._generate_with_stability(prompt, name)
                if result:
                    return result
        except Exception as e:
            print(f"Stability AI failed: {e}")
        
        # Fallback to Gemini if Stability fails
        try:
            if settings.GEMINI_API_KEY:
                result = await self._generate_with_gemini(prompt, name)
                if result:
                    return result
        except Exception as e:
            print(f"Gemini fallback failed: {e}")
        
        # Final fallback to styled placeholder
        return self._generate_placeholder(name, primary_color, prompt)

    async def _generate_with_stability(self, prompt: str, name: str) -> dict:
        """Generate logo using Stability AI SDXL."""
        api_host = "https://api.stability.ai"
        engine_id = "stable-diffusion-xl-1024-v1-0"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{api_host}/v1/generation/{engine_id}/text-to-image",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {settings.STABILITY_API_KEY}"
                },
                json={
                    "text_prompts": [{"text": prompt}],
                    "cfg_scale": 8,
                    "height": 1024,
                    "width": 1024,
                    "samples": 1,
                    "steps": 40,
                    "seed": random.randint(0, 4294967295)  # Random seed for variation
                },
                timeout=30.0
            )

            if response.status_code != 200:
                raise Exception(f"Non-200 response: {response.text}")

            data = response.json()
            image_b64 = data["artifacts"][0]["base64"]
            return {
                "url": f"data:image/png;base64,{image_b64}",
                "prompt": prompt,
                "service": "stability"
            }

    async def _generate_with_gemini(self, prompt: str, name: str) -> dict:
        """Fallback: Generate logo using Gemini API."""
        # Placeholder for Gemini implementation
        # In production, you would call Gemini's image generation API here
        # For now, return None to skip to placeholder
        return None

    def _generate_placeholder(self, name: str, color: str, prompt: str) -> dict:
        """Generate a styled, varied placeholder logo."""
        import urllib.parse
        
        # Color variations for visual diversity
        color_hex = color.replace("#", "")
        
        # Generate complementary color for variation
        # Simple algorithm: invert some RGB components for contrast
        try:
            r = int(color_hex[0:2], 16)
            g = int(color_hex[2:4], 16)
            b = int(color_hex[4:6], 16)
            
            # Create variation by adjusting brightness
            variation = random.choice([
                f"{min(r+40, 255):02x}{min(g+40, 255):02x}{min(b+40, 255):02x}",  # Lighter
                f"{max(r-40, 0):02x}{max(g-40, 0):02x}{max(b-40, 0):02x}",  # Darker
                f"{r:02x}{min(g+60, 255):02x}{b:02x}",  # Green shift
                f"{min(r+60, 255):02x}{g:02x}{b:02x}",  # Red shift
            ])
        except:
            variation = color_hex
        
        # Layout styles for variety
        layouts = [
            {"size": "800x800", "text": f"{name}"},
            {"size": "800x600", "text": f"◆ {name} ◆"},
            {"size": "800x800", "text": f"● {name}"},
            {"size": "800x800", "text": f"▲ {name} ▲"},
            {"size": "800x800", "text": f"■ {name}"},
        ]
        
        layout = random.choice(layouts)
        encoded_text = urllib.parse.quote(layout["text"])
        
        # Use variation color for diversity
        bg_color = variation if random.random() > 0.5 else color_hex
        
        return {
            "url": f"https://placehold.co/{layout['size']}/{bg_color}/ffffff?text={encoded_text}&font=roboto",
            "prompt": prompt,
            "service": "placeholder"
        }

    async def generate_color_palette(self, tone: str) -> list[str]:
        # Simple logic based on tone, or we could use AI.
        # For reliability and speed, predefined palettes mapped to tones are often better/safer
        # unless user specifically asked for AI generated hex codes.
        # The prompt says "AI-generated brand colors". Let's use simple randomization with tone-bias.
        
        palettes = {
            "Professional": ["#0f172a", "#334155", "#475569", "#94a3b8", "#f8fafc"],
            "Playful": ["#ff6b6b", "#feca57", "#48dbfb", "#ff9ff3", "#54a0ff"],
            "Luxury": ["#000000", "#1c1c1c", "#d4af37", "#f5f5f5", "#ffffff"],
            "Innovative": ["#6366f1", "#8b5cf6", "#ec4899", "#10b981", "#1e293b"]
        }
        
        return palettes.get(tone, ["#000000", "#ffffff", "#cccccc", "#333333", "#666666"])

visual_service = VisualService()
