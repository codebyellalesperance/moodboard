import json
from datetime import datetime
import openai
from config import Config

# Initialize OpenAI client
client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)


def get_current_season() -> str:
    """Get the current season based on date (Northern Hemisphere)."""
    month = datetime.now().month
    if month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    elif month in [9, 10, 11]:
        return "fall"
    else:
        return "winter"


# Style archetypes for classification
STYLE_ARCHETYPES = [
    "minimalist", "maximalist", "boho", "classic", "romantic",
    "edgy", "sporty", "preppy", "glamorous", "artsy",
    "streetwear", "cottagecore", "dark academia", "coastal",
    "old money", "quiet luxury", "y2k", "grunge", "vintage"
]

# Occasion categories
OCCASION_TYPES = [
    "everyday casual", "workwear", "business casual", "formal/evening",
    "date night", "vacation/resort", "weekend brunch", "outdoor/active",
    "wedding guest", "party/going out"
]

# Editorial-approved brands by aesthetic (Vogue, Instagram, TikTok trending)
# These are brands that consistently appear in fashion editorials and trend content
EDITORIAL_BRANDS = {
    "quiet luxury": {
        "aspirational": ["The Row", "Loro Piana", "Brunello Cucinelli", "Toteme", "Khaite"],
        "contemporary": ["COS", "Vince", "Theory", "Anine Bing", "Nili Lotan"],
        "trending": ["Posse", "St. Agni", "Bite Studios", "Róhe", "Fforme"]
    },
    "minimalist": {
        "aspirational": ["Jil Sander", "Lemaire", "The Row", "Acne Studios", "Maison Margiela"],
        "contemporary": ["COS", "Arket", "& Other Stories", "Everlane", "Aritzia"],
        "trending": ["Frankie Shop", "Low Classic", "Amomento", "Baserange", "Deveaux"]
    },
    "boho": {
        "aspirational": ["Isabel Marant", "Ulla Johnson", "Zimmermann", "Etro", "Chloé"],
        "contemporary": ["Free People", "Dôen", "Sézane", "Spell", "Farm Rio"],
        "trending": ["Alemais", "Johanna Ortiz", "Aje", "Sir The Label", "Cult Gaia"]
    },
    "old money": {
        "aspirational": ["Ralph Lauren", "Loro Piana", "Brunello Cucinelli", "Max Mara", "Burberry"],
        "contemporary": ["J.Crew", "Polo Ralph Lauren", "Vineyard Vines", "Brooks Brothers", "Massimo Dutti"],
        "trending": ["Kule", "Alex Mill", "La Ligne", "G. Label", "Rag & Bone"]
    },
    "streetwear": {
        "aspirational": ["Off-White", "Fear of God", "Balenciaga", "Vetements", "Palm Angels"],
        "contemporary": ["Stüssy", "Aimé Leon Dore", "Kith", "Carhartt WIP", "Palace"],
        "trending": ["Corteiz", "Aries", "Brain Dead", "Online Ceramics", "Madhappy"]
    },
    "coquette": {
        "aspirational": ["Simone Rocha", "Cecilie Bahnsen", "Miu Miu", "Sandy Liang", "Shushu/Tong"],
        "contemporary": ["For Love & Lemons", "Reformation", "Rouje", "Realisation Par", "House of CB"],
        "trending": ["Mirror Palais", "Orseund Iris", "Rat & Boa", "Danielle Guizio", "Are You Am I"]
    },
    "dark academia": {
        "aspirational": ["Burberry", "Ralph Lauren", "Margaret Howell", "Maison Margiela", "Bottega Veneta"],
        "contemporary": ["Sandro", "Maje", "AllSaints", "Reiss", "Massimo Dutti"],
        "trending": ["Story MFG", "Auralee", "Lemaire", "Our Legacy", "De Bonne Facture"]
    },
    "coastal": {
        "aspirational": ["Loro Piana", "Brunello Cucinelli", "Zimmermann", "Valentino", "Chloé"],
        "contemporary": ["Faithfull the Brand", "Reformation", "Aritzia", "Abercrombie", "J.Crew"],
        "trending": ["Posse", "Sir The Label", "Matteau", "Bondi Born", "Esse Studios"]
    },
    "y2k": {
        "aspirational": ["Blumarine", "Roberto Cavalli", "Versace", "Dior", "Dolce & Gabbana"],
        "contemporary": ["Juicy Couture", "Jaded London", "I.AM.GIA", "MIAOU", "Poster Girl"],
        "trending": ["Charlotte Knowles", "Masha Popova", "Aya Muse", "LaQuan Smith", "KNWLS"]
    },
    "edgy": {
        "aspirational": ["Rick Owens", "Ann Demeulemeester", "Alexander McQueen", "Mugler", "Balenciaga"],
        "contemporary": ["AllSaints", "The Kooples", "Helmut Lang", "Ksubi", "R13"],
        "trending": ["Dion Lee", "Ottolinger", "Misbhv", "Marques Almeida", "Heron Preston"]
    },
    "romantic": {
        "aspirational": ["Zimmermann", "Valentino", "Giambattista Valli", "Rodarte", "Oscar de la Renta"],
        "contemporary": ["Self-Portrait", "Needle & Thread", "LoveShackFancy", "Reformation", "Veronica Beard"],
        "trending": ["Selkie", "Hill House Home", "Sister Jane", "Batsheva", "Markarian"]
    },
    "tropical": {
        "aspirational": ["Zimmermann", "Johanna Ortiz", "Adriana Degreas", "Agua by Agua Bendita", "Cult Gaia"],
        "contemporary": ["Farm Rio", "Solid & Striped", "Faithfull the Brand", "Mara Hoffman", "Miguelina"],
        "trending": ["Hunza G", "Frankies Bikinis", "Montce", "Vitamin A", "Agua Bendita"]
    },
    "athleisure": {
        "aspirational": ["Lululemon", "Alo Yoga", "Varley", "Splits59", "Lucas Hugh"],
        "contemporary": ["Girlfriend Collective", "Outdoor Voices", "Vuori", "Beyond Yoga", "Sweaty Betty"],
        "trending": ["Set Active", "Avia", "Tala", "Year of Ours", "P.E Nation"]
    },
    "western": {
        "aspirational": ["Ralph Lauren", "Isabel Marant", "Etro", "Chloe", "Coach"],
        "contemporary": ["Free People", "Understated Leather", "Tecovas", "Lucchese", "Double D Ranch"],
        "trending": ["Miron Crosby", "City Boots", "Brother Vellies", "R13", "Ganni"]
    },
    "parisian": {
        "aspirational": ["Celine", "The Row", "Isabel Marant", "Chanel", "Saint Laurent"],
        "contemporary": ["Sezane", "Rouje", "Ba&sh", "Maje", "Sandro"],
        "trending": ["Musier Paris", "Jacquemus", "Lemaire", "The Frankie Shop", "Toteme"]
    },
    "glamorous": {
        "aspirational": ["Versace", "Dolce & Gabbana", "Balmain", "Tom Ford", "Saint Laurent"],
        "contemporary": ["Retrofete", "Nadine Merabi", "Bronx and Banco", "Zhivago", "Amanda Uprichard"],
        "trending": ["LaQuan Smith", "David Koma", "Alex Perry", "Magda Butrym", "16Arlington"]
    },
    "mob wife": {
        "aspirational": ["Dolce & Gabbana", "Versace", "Roberto Cavalli", "Tom Ford", "Max Mara"],
        "contemporary": ["Nili Lotan", "The Mannei", "Anine Bing", "Stand Studio", "Apparis"],
        "trending": ["Weworewhat", "House of Sunny", "I.AM.GIA", "Poster Girl", "Miaou"]
    },
    "cottagecore": {
        "aspirational": ["Zimmermann", "Ulla Johnson", "Doen", "Brock Collection", "Erdem"],
        "contemporary": ["Christy Dawn", "Doen", "Hill House Home", "Reformation", "Sezane"],
        "trending": ["Lirika Matoshi", "Selkie", "Sister Jane", "Nobody's Child", "& Other Stories"]
    },
    "scandinavian": {
        "aspirational": ["Toteme", "Acne Studios", "Ganni", "The Row", "Jil Sander"],
        "contemporary": ["COS", "Arket", "& Other Stories", "Filippa K", "Holzweiler"],
        "trending": ["Cecilie Bahnsen", "Stine Goya", "Rotate", "Remain Birger Christensen", "Rodebjer"]
    },
    "corporate": {
        "aspirational": ["The Row", "Max Mara", "Loro Piana", "Bottega Veneta", "Celine"],
        "contemporary": ["Theory", "Vince", "Reiss", "Hugo Boss", "Argent"],
        "trending": ["Frankie Shop", "Esse Studios", "Low Classic", "Gauge81", "St. Agni"]
    }
}

# TikTok/Instagram trending modifiers for search queries
TREND_MODIFIERS = [
    "trending", "viral", "aesthetic", "influencer favorite",
    "editor pick", "street style", "runway inspired"
]

# JSON schema for mood profile (shared between prompts)
MOOD_JSON_SCHEMA = """
Return a JSON object with EXACTLY these fields (no additional text, just JSON):

{{
  "name": "A catchy 2-5 word aesthetic name (e.g., 'Coastal Grandmother', 'Old Money Tennis', '90s Minimalist', 'Dark Academia')",

  "mood": "5-8 words describing the emotional energy (e.g., 'Effortless, polished, confident')",

  "gender": "women | men | unisex (infer from images/prompt, default to 'women' if unclear)",

  "style_archetype": {{
    "primary": "The dominant style archetype (e.g., 'minimalist', 'boho', 'dark academia', 'old money')",
    "secondary": "A complementary style influence, or null if pure single style",
    "description": "1-2 sentences explain
    
    ing how these archetypes manifest in this specific aesthetic"
  }},

  "occasions": [
    "Primary occasion this vibe suits (e.g., 'everyday casual', 'workwear', 'date night')",
    "Secondary occasion if applicable"
  ],

  "season": {{
    "best_for": ["season1", "season2"],
    "adaptable": true,
    "current_season_tips": "Brief tip for wearing this aesthetic in {current_season}"
  }},

  "color_palette": [
    {{"name": "Color name", "hex": "#HEXCODE"}},
    {{"name": "Another color", "hex": "#HEXCODE"}}
  ],

  "textures": ["texture1", "texture2", "texture3", "texture4"],

  "key_pieces": [
    "Specific item 1 (e.g., 'oversized linen blazer')",
    "Specific item 2",
    "Specific item 3",
    "Specific item 4",
    "Specific item 5"
  ],

  "avoid": ["thing1", "thing2", "thing3"],

  "target_brands": {{
    "aspirational": ["Luxury/designer brand featured in Vogue editorials", "Another fashion house that defines this aesthetic"],
    "contemporary": ["Fashion-forward mid-range brand seen on influencers", "Another editorial-approved contemporary brand"],
    "trending": ["TikTok/Instagram viral brand that's having a moment", "Another emerging designer or cult favorite"],
  }},

  "search_queries": [
    "tops query with trend modifier (e.g., 'trending silk blouse women')",
    "bottoms query (e.g., 'wide leg tailored trousers women')",
    "dress or jumpsuit query with aesthetic (e.g., 'minimalist midi dress designer')",
    "outerwear query (e.g., 'oversized wool coat editorial')",
    "shoes query with style (e.g., 'trending ballet flats leather')",
    "bag query (e.g., 'quiet luxury shoulder bag')",
    "jewelry query (e.g., 'gold vermeil earrings minimal')",
    "brand-specific query (e.g., 'Reformation dress', 'COS blazer')",
    "trending item query (e.g., 'barrel jeans', 'mesh ballet flats')",
    "additional accessory query"
  ],

  "confidence": {{
    "overall": 0.85,
    "aesthetic_clarity": 0.9,
    "color_accuracy": 0.85,
    "brand_match": 0.8,
    "notes": "Brief note if confidence is low in any area, or null if high confidence"
  }}
}}

Important rules:
- gender should be "women", "men", or "unisex" - infer from visible clothing/context, default to "women"
- style_archetype.primary must be one of: minimalist, maximalist, boho, classic, romantic, edgy, sporty, preppy, glamorous, artsy, streetwear, cottagecore, dark academia, coastal, old money, quiet luxury, y2k, grunge, vintage
- occasions should have 1-3 items from: everyday casual, workwear, business casual, formal/evening, date night, vacation/resort, weekend brunch, outdoor/active, wedding guest, party/going out
- season.best_for should list 1-2 seasons (spring, summer, fall, winter); season.adaptable indicates if it works year-round with modifications
- color_palette should have 4-6 colors
- textures should have 4-6 items
- key_pieces should have 5-7 specific, editorial-worthy items (not generic basics)
- avoid should have 3-5 items that would cheapen or misrepresent the aesthetic

BRAND QUALITY STANDARDS (CRITICAL):
- Think VOGUE EDITORIAL, not fast fashion. Every brand should be one you'd see in a fashion magazine or on a style influencer.
- target_brands should have 2-3 brands per tier that are GENUINELY fashion-forward:
  - Aspirational: Brands featured in Vogue, Harper's Bazaar, worn by celebrities (The Row, Khaite, Toteme, Zimmermann, Isabel Marant)
  - Contemporary: Instagram/influencer favorites with strong design DNA (Reformation, Aritzia, COS, Anine Bing, Sézane, Réalisation Par)
  - Trending: TikTok viral brands, emerging designers, cult favorites (Frankie Shop, Mirror Palais, Posse, Sir The Label, Cult Gaia)
- AVOID suggesting: Shein, Romwe, Fashion Nova, generic Amazon brands, or anything that looks cheap
- Include at least 2 brand-specific search queries (e.g., "Reformation midi dress", "COS wool coat")

SEARCH QUERY STANDARDS:
- search_queries MUST have 10-12 queries covering: tops, bottoms, dresses, outerwear, shoes, bags, jewelry, plus 2-3 brand-specific and trending item queries
- Each query should sound like a fashion editor's search, NOT a generic shopping query
- Include trend modifiers: "trending", "viral", "aesthetic", "editorial", "designer inspired", "street style"
- Include specific trending items when relevant: barrel jeans, mesh flats, cherry red bag, butter yellow, etc.
- 2-3 queries should include specific brand names from the target_brands list
- If user mentioned budget constraints, include "under $X" but still prioritize quality over cheap

- confidence scores should be 0.0-1.0; be honest about uncertainty
- Return ONLY the JSON object, no markdown code blocks, no explanation
"""

MOOD_EXTRACTION_PROMPT_WITH_IMAGES = """
Analyze these images together as a single mood board. The user wants to shop this vibe.

User's request: {user_prompt}
Current season: {current_season}

You are a FASHION EDITOR at Vogue. Your task: Extract the AESTHETIC ESSENCE — not what's literally in the image, but the FEELING and STYLE ENERGY someone would want to recreate.

Think about:
- What would a stylist pull for this shoot?
- What brands would a fashion influencer tag in this post?
- What items are trending on TikTok/Instagram that match this vibe?
- What would make this look magazine-worthy, not mall-brand generic?

Recommend ONLY editorial-quality, fashion-forward pieces and brands. No fast fashion, no generic basics. Every item should feel intentional and stylish.
""" + MOOD_JSON_SCHEMA

MOOD_EXTRACTION_PROMPT_TEXT_ONLY = """
The user wants to shop a specific vibe/aesthetic. Based on their description, create a mood profile.

User's vibe description: {user_prompt}
Current season: {current_season}

You are a FASHION EDITOR at Vogue. Your task: Interpret their aesthetic vision and create a comprehensive style profile that captures the FEELING and STYLE ENERGY they want to achieve.

Think about:
- What would a stylist pull for this aesthetic?
- What brands would a fashion influencer recommend?
- What items are trending on TikTok/Instagram that match this vibe?
- What would make this look magazine-worthy, not mall-brand generic?

Recommend ONLY editorial-quality, fashion-forward pieces and brands. No fast fashion, no generic basics. Every item should feel intentional and stylish.
""" + MOOD_JSON_SCHEMA


def extract_mood(images: list, prompt: str = "") -> dict:
    """
    Extract mood profile from images and/or text prompt.

    Args:
        images: List of base64 encoded images with data URI prefix (can be empty)
        prompt: User's vibe description (can be empty if images provided)

    Returns:
        Parsed mood profile dict with fields:
        - name, mood, gender, style_archetype, occasions, season
        - color_palette, textures, key_pieces, avoid, target_brands
        - search_queries, confidence

    Raises:
        Exception: If API call fails or response parsing fails
    """
    has_images = images and len(images) > 0
    current_season = get_current_season()

    # Build message content
    content = []

    # Add images if provided
    if has_images:
        for img in images:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": img,
                    "detail": "high"
                }
            })

    # Choose prompt based on whether we have images
    if has_images:
        formatted_prompt = MOOD_EXTRACTION_PROMPT_WITH_IMAGES.format(
            user_prompt=prompt if prompt else "No specific modifications requested",
            current_season=current_season
        )
    else:
        formatted_prompt = MOOD_EXTRACTION_PROMPT_TEXT_ONLY.format(
            user_prompt=prompt,
            current_season=current_season
        )

    content.append({
        "type": "text",
        "text": formatted_prompt
    })

    # Call OpenAI - use gpt-4o for images, gpt-4o for text-only too (good at style)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": content
            }
        ],
        max_tokens=2000,
        temperature=0.7
    )

    # Extract response text
    response_text = response.choices[0].message.content

    # Clean up response (sometimes GPT adds markdown code blocks)
    response_text = clean_json_response(response_text)

    # Parse JSON
    try:
        mood_profile = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse mood profile JSON: {e}\nResponse was: {response_text[:500]}")

    # Validate required fields
    required_fields = ['name', 'mood', 'color_palette', 'textures', 'key_pieces', 'avoid', 'search_queries']
    for field in required_fields:
        if field not in mood_profile:
            raise Exception(f"Mood profile missing required field: {field}")

    # Ensure target_brands exists with fallback structure including trending tier
    if 'target_brands' not in mood_profile:
        mood_profile['target_brands'] = {
            'aspirational': [],
            'contemporary': [],
            'trending': [],
        }
    elif 'trending' not in mood_profile['target_brands']:
        # Add trending tier if missing from response
        mood_profile['target_brands']['trending'] = []

    # Ensure gender exists with fallback
    if 'gender' not in mood_profile:
        mood_profile['gender'] = 'women'

    # Ensure style_archetype exists with fallback
    if 'style_archetype' not in mood_profile:
        mood_profile['style_archetype'] = {
            'primary': 'classic',
            'secondary': None,
            'description': 'A versatile, timeless aesthetic'
        }

    # Ensure occasions exists with fallback
    if 'occasions' not in mood_profile:
        mood_profile['occasions'] = ['everyday casual']

    # Ensure season exists with fallback
    if 'season' not in mood_profile:
        mood_profile['season'] = {
            'best_for': [current_season],
            'adaptable': True,
            'current_season_tips': None
        }

    # Ensure confidence exists with fallback
    if 'confidence' not in mood_profile:
        mood_profile['confidence'] = {
            'overall': 0.7,
            'aesthetic_clarity': 0.7,
            'color_accuracy': 0.7,
            'brand_match': 0.7,
            'notes': 'Confidence scores not provided by model'
        }

    return mood_profile


def clean_json_response(text: str) -> str:
    """
    Clean up GPT response to extract pure JSON.

    Args:
        text: Raw response text

    Returns:
        Cleaned JSON string
    """
    text = text.strip()

    # Remove markdown code blocks
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()
