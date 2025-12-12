import json
import openai
from config import Config

# Initialize OpenAI client
client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)

MOOD_EXTRACTION_PROMPT = """
Analyze these images together as a single mood board. The user wants to shop this vibe.

User's request: {user_prompt}

Your task: Extract the AESTHETIC ESSENCE — not what's literally in the image, but the FEELING and STYLE ENERGY someone would want to recreate through clothing and accessories.

Return a JSON object with EXACTLY these fields (no additional text, just JSON):

{{
  "name": "A catchy 2-5 word aesthetic name (e.g., 'Coastal Grandmother', 'Old Money Tennis', '90s Minimalist', 'Dark Academia')",

  "mood": "2-4 words describing the emotional energy (e.g., 'Effortless, polished, confident')",

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

  "search_queries": [
    "specific searchable product query 1",
    "specific searchable product query 2",
    "specific searchable product query 3",
    "specific searchable product query 4",
    "specific searchable product query 5",
    "specific searchable product query 6",
    "specific searchable product query 7",
    "specific searchable product query 8"
  ]
}}

Important rules:
- color_palette should have 4-6 colors
- textures should have 4-6 items
- key_pieces should have 5-7 items
- avoid should have 3-5 items
- search_queries should have 8-12 specific product searches
- search_queries should be specific enough to find real products (e.g., "cream oversized linen blazer women" not just "blazer")
- If user mentioned budget constraints, include "affordable" or "under $X" in some queries
- Return ONLY the JSON object, no markdown code blocks, no explanation
"""


def extract_mood(images: list, prompt: str = "") -> dict:
    """
    Send images to GPT-4V and extract mood profile.

    Args:
        images: List of base64 encoded images with data URI prefix
        prompt: User's optional modifier prompt

    Returns:
        Parsed mood profile dict

    Raises:
        Exception: If API call fails or response parsing fails
    """

    # Build message content with images
    content = []

    # Add each image
    for img in images:
        content.append({
            "type": "image_url",
            "image_url": {
                "url": img,
                "detail": "high"
            }
        })

    # Add the text prompt
    formatted_prompt = MOOD_EXTRACTION_PROMPT.format(
        user_prompt=prompt if prompt else "No specific modifications requested"
    )
    content.append({
        "type": "text",
        "text": formatted_prompt
    })

    # Call GPT-4V
    response = client.chat.completions.create(
        model="gpt-4o",  # or "gpt-4-vision-preview"
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
