"""GPT-4V integration for mood extraction from images."""

import json
import re
from openai import OpenAI
from config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

MOOD_EXTRACTION_PROMPT = """Analyze these inspiration images and extract the aesthetic mood/vibe.

Return a JSON object with:
{
    "name": "Short aesthetic name (e.g., 'Coastal Grandmother', 'Dark Academia')",
    "mood": "2-4 word mood description",
    "color_palette": [{"name": "Color name", "hex": "#hexcode"}, ...] (3-5 colors),
    "textures": ["texture1", "texture2", ...] (3-5 textures),
    "key_pieces": ["piece1", "piece2", ...] (4-6 clothing/accessory types),
    "avoid": ["thing1", "thing2"] (2-3 things that don't fit this aesthetic),
    "search_queries": ["query1", "query2", ...] (5-8 specific shopping search queries)
}

Make the search_queries specific and shoppable, like "oversized linen blazer women" or "chunky gold hoop earrings".
Focus on the FEELING and ENERGY of the images, not just copying exact items.
Return ONLY valid JSON, no markdown or explanation."""


def extract_mood(images: list[str], prompt: str = '') -> dict:
    """
    Send images to GPT-4V and extract mood profile.

    Args:
        images: List of base64 data URI strings
        prompt: Optional user prompt for context

    Returns:
        Mood profile dict with name, colors, textures, key_pieces, search_queries
    """
    # Build message content with images
    content = []
    for image_uri in images:
        content.append({
            'type': 'image_url',
            'image_url': {'url': image_uri}
        })

    # Add the prompt
    full_prompt = MOOD_EXTRACTION_PROMPT
    if prompt:
        full_prompt += f'\n\nUser context: {prompt}'

    content.append({
        'type': 'text',
        'text': full_prompt
    })

    # Call GPT-4V
    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[{
            'role': 'user',
            'content': content
        }],
        max_tokens=2000
    )

    # Parse response
    result_text = response.choices[0].message.content

    # Strip markdown code blocks if present
    result_text = re.sub(r'^```json\s*', '', result_text)
    result_text = re.sub(r'\s*```$', '', result_text)

    return json.loads(result_text)
