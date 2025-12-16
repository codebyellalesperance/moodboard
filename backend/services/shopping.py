import re
import json
import logging
import openai
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from serpapi import GoogleSearch
from config import Config

logger = logging.getLogger(__name__)

# Initialize OpenAI client for re-ranking
client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)

# Trusted retailers for quality filtering
TRUSTED_RETAILERS = {
    # Fast fashion
    "zara", "h&m", "mango", "cos", "& other stories", "uniqlo", "asos", "topshop",
    # Mid-range
    "nordstrom", "nordstrom rack", "bloomingdale's", "saks fifth avenue", "neiman marcus",
    "revolve", "shopbop", "free people", "anthropologie", "urban outfitters",
    "reformation", "everlane", "j.crew", "banana republic", "gap", "old navy",
    # Luxury
    "net-a-porter", "ssense", "farfetch", "mytheresa", "matches fashion",
    "luisaviaroma", "browns", "bergdorf goodman",
    # Department stores
    "macy's", "dillard's", "belk", "kohl's", "jcpenney", "target", "walmart",
    # Specialty
    "lululemon", "nike", "adidas", "alo yoga", "athleta", "outdoor voices",
    "patagonia", "rei", "the north face",
    # Online
    "amazon", "amazon.com", "zappos", "6pm", "poshmark", "ebay"
}

# Curated premium brands - quality across price points
CURATED_BRANDS = {
    # Contemporary
    "aritzia", "reformation", "cos", "everlane", "theory", "vince",
    "eileen fisher", "frame", "agolde", "citizens of humanity",
    "mother", "rag & bone", "all saints", "reiss", "sandro", "maje",
    "ba&sh", "ted baker", "equipment", "joie",
    # Premium Denim
    "ag jeans", "paige", "dl1961", "j brand", "hudson",
    # Luxury Accessible
    "tory burch", "kate spade", "coach", "marc jacobs", "madewell"
}

# Editorial brands - frequently featured in Vogue, Elle, Harper's Bazaar
EDITORIAL_BRANDS = {
    # High Fashion
    "the row", "toteme", "jacquemus", "khaite", "ganni", "nanushka",
    "staud", "cult gaia", "by far", "mansur gavriel", "jil sander",
    "lemaire", "acne studios", "isabel marant", "zimmermann",
    # Designer
    "bottega veneta", "loewe", "celine", "the frankie shop",
    "rohe", "st. agni", "esse studios", "co",
    # Trending Editorial
    "alaia", "coperni", "self-portrait", "magda butrym", "rotate"
}


def search_products(
    query: str,
    num_results: int = 10,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None
) -> List[Dict]:
    """
    Search Google Shopping via SerpApi for products.
    """
    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": Config.SERPAPI_KEY,
        "num": min(num_results, 40),
        "gl": "us",
        "hl": "en"
    }

    # Add price filters if specified
    if min_price is not None:
        params["tbs"] = f"mr:1,price:1,ppr_min:{min_price}"
    if max_price is not None:
        existing_tbs = params.get("tbs", "mr:1,price:1")
        params["tbs"] = f"{existing_tbs},ppr_max:{max_price}"

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
    except Exception as e:
        logger.error(f"SerpApi error: {e}")
        return []

    products = []
    for item in results.get("shopping_results", []):
        product = format_product(item, query)
        if product:
            products.append(product)

    return products


def format_product(item: dict, query: str) -> Optional[Dict]:
    """
    Format a SerpApi Google Shopping product into our standard format.
    """
    try:
        # Parse price (comes as string like "$89.99" or "89.99")
        price_str = item.get("price", item.get("extracted_price", "0"))
        if isinstance(price_str, str):
            price = float(re.sub(r'[^\d.]', '', price_str) or 0)
        else:
            price = float(price_str or 0)

        # Get original price if on sale
        original_price = price
        if "original_price" in item:
            orig_str = item["original_price"]
            if isinstance(orig_str, str):
                original_price = float(re.sub(r'[^\d.]', '', orig_str) or price)
            else:
                original_price = float(orig_str or price)

        retailer = item.get("source", "").strip()

        return {
            "id": f"gshop_{item.get('product_id', item.get('position', ''))}",
            "name": item.get("title", "Unknown Product"),
            "brand": item.get("brand", extract_brand(item.get("title", ""))),
            "price": round(price, 2),
            "original_price": round(original_price, 2),
            "on_sale": price < original_price,
            "currency": "USD",
            "image_url": item.get("thumbnail", ""),
            "product_url": item.get("link", ""),
            "retailer": retailer,
            "category": "",
            "match_reason": query,
            "in_stock": True
        }
    except Exception as e:
        logger.error(f"Error formatting product: {e}")
        return None


def extract_brand(title: str) -> str:
    """Extract brand name from product title (usually first word/phrase)."""
    if not title:
        return ""
    # Common patterns: "Brand Name - Product" or "Brand Product"
    parts = title.split(" - ")
    if len(parts) > 1:
        return parts[0].strip()
    # Just return first 2 words as potential brand
    words = title.split()[:2]
    return " ".join(words) if words else ""


def is_trusted_retailer(retailer: str) -> bool:
    """Check if retailer is in our trusted list."""
    retailer_lower = retailer.lower().strip()
    for trusted in TRUSTED_RETAILERS:
        if trusted in retailer_lower or retailer_lower in trusted:
            return True
    return False


def get_brand_score(brand: str) -> int:
    """
    Score brand based on curation lists.
    Returns: 0=unknown, 1=curated, 2=editorial, 3=both
    """
    if not brand:
        return 0
    brand_lower = brand.lower().strip()
    in_curated = any(c in brand_lower or brand_lower in c for c in CURATED_BRANDS)
    in_editorial = any(e in brand_lower or brand_lower in e for e in EDITORIAL_BRANDS)
    if in_curated and in_editorial:
        return 3
    elif in_editorial:
        return 2
    elif in_curated:
        return 1
    return 0


def enhance_queries_with_modifiers(queries: List[str]) -> List[str]:
    """
    Enhance search queries with trending, editorial, and statement piece modifiers.

    Distribution:
    - Queries 1-2: Add "trending" prefix
    - Queries 3-4: Add editorial modifier
    - Queries 5-6: Add statement/unique modifier
    """
    if not queries:
        return queries
    enhanced = []
    editorial_modifiers = ["vogue approved", "as seen in magazine"]
    statement_modifiers = ["statement piece", "unique designer"]
    for i, query in enumerate(queries[:6]):
        if i < 2:
            enhanced.append(f"trending {query}")
        elif i < 4:
            enhanced.append(f"{query} {editorial_modifiers[i - 2]}")
        else:
            enhanced.append(f"{statement_modifiers[i - 4]} {query}")
    return enhanced


def search_all_queries(
    search_queries: List[str],
    max_products: int = 20,
    budget: Optional[str] = None,
    vibe_profile: Optional[Dict] = None
) -> List[Dict]:
    """
    Search multiple queries, filter, re-rank with AI, and return best matches.
    """
    all_products = []
    seen_ids = set()

    # Set price filters based on budget
    min_price, max_price = None, None
    if budget == "affordable":
        max_price = 75
    elif budget == "mid-range":
        min_price = 50
        max_price = 200
    elif budget == "luxury":
        min_price = 150

    # Use up to 6 queries, enhanced with trending/editorial modifiers
    queries_to_use = enhance_queries_with_modifiers(search_queries[:6])
    logger.info(f"Enhanced queries: {queries_to_use}")
    products_per_query = 10  # Get 10 products per query

    # Run all queries in parallel for speed
    def fetch_query(query):
        try:
            return search_products(
                query=query,
                num_results=products_per_query,
                min_price=min_price,
                max_price=max_price
            )
        except Exception as e:
            logger.error(f"Error searching '{query}': {e}")
            return []

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(fetch_query, q): q for q in queries_to_use}
        for future in as_completed(futures):
            products = future.result()
            for product in products:
                product_key = product["id"] + product.get("product_url", "")
                if product_key not in seen_ids:
                    seen_ids.add(product_key)
                    # Add brand score for curated/editorial brand boosting
                    product["brand_score"] = get_brand_score(product.get("brand", ""))
                    all_products.append(product)

    logger.info(f"Fetched {len(all_products)} total products from {len(queries_to_use)} parallel queries")

    # Filter to trusted retailers
    trusted_products = [p for p in all_products if is_trusted_retailer(p.get("retailer", ""))]
    logger.info(f"After retailer filter: {len(trusted_products)} products")

    # If we filtered too aggressively, keep some untrusted ones
    if len(trusted_products) < 10 and len(all_products) > len(trusted_products):
        untrusted = [p for p in all_products if p not in trusted_products]
        trusted_products.extend(untrusted[:10 - len(trusted_products)])

    # AI re-ranking if we have a vibe profile
    if vibe_profile and len(trusted_products) > 0:
        trusted_products = rerank_products_with_ai(trusted_products, vibe_profile)
        logger.info(f"After AI re-ranking: {len(trusted_products)} products")

    # Sort: by vibe score (highest first), then brand score, then on-sale, then by price
    trusted_products.sort(key=lambda x: (
        -x.get("vibe_score", 5),     # Higher vibe scores first
        -x.get("brand_score", 0),    # Higher brand scores second
        not x.get("on_sale", False), # Sale items third
        x.get("price", 0)            # Lower prices last
    ))

    return trusted_products[:max_products]


def rerank_products_with_ai(products: List[Dict], vibe_profile: Dict) -> List[Dict]:
    """
    Use GPT to score products for how well they match the vibe.
    Returns products with score >= 6, sorted by score descending.
    """
    if not products:
        return []

    # Limit to 30 products to control costs
    products_to_score = products[:30]

    # Build product list for GPT
    product_list = []
    for i, p in enumerate(products_to_score):
        product_list.append({
            "index": i,
            "name": p.get("name", ""),
            "brand": p.get("brand", ""),
            "retailer": p.get("retailer", ""),
            "price": p.get("price", 0)
        })

    # Build brand guidance for AI
    curated_sample = ", ".join(list(CURATED_BRANDS)[:8])
    editorial_sample = ", ".join(list(EDITORIAL_BRANDS)[:8])

    prompt = f"""You are a fashion stylist and editor curating products for a client. Score how well each product fits this aesthetic:

AESTHETIC: {vibe_profile.get('name', 'Unknown')}
MOOD: {vibe_profile.get('mood', '')}
KEY PIECES: {', '.join(vibe_profile.get('key_pieces', []))}
TEXTURES: {', '.join(vibe_profile.get('textures', []))}
AVOID: {', '.join(vibe_profile.get('avoid', []))}

BRAND PREFERENCES (give +1 boost to these):
- Premium/Curated: {curated_sample}, etc.
- Editorial/Fashion-Forward: {editorial_sample}, etc.

PRODUCTS:
{json.dumps(product_list, indent=2)}

Score each product 1-10:
- 9-10: Perfect fit + premium/editorial brand OR unique statement piece
- 8: Perfect aesthetic fit
- 6-7: Good fit, would work well in this wardrobe
- 4-5: Neutral, could work but not ideal
- 1-3: Wrong aesthetic, doesn't belong

SCORING GUIDANCE:
- Balance basics with STATEMENT PIECES - we want some showstoppers and conversation starters
- Give +1 boost to unique, niche, or artisan items that stand out
- Give +1 boost to recognized premium or editorial brands
- Prioritize VARIETY - we want tops, bottoms, dresses, shoes, accessories
- Look for interesting details: unusual silhouettes, bold colors, unique textures, architectural designs
- Include some avant-garde or fashion-forward pieces alongside wearable basics

Return ONLY a JSON array: [{{"index": 0, "score": 7}}, {{"index": 1, "score": 4}}]"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use mini for cost efficiency
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.3
        )

        response_text = response.choices[0].message.content.strip()

        # Clean up response
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        response_text = response_text.strip()

        scores = json.loads(response_text)

        # Build score map
        score_map = {item["index"]: item["score"] for item in scores}

        # Filter and sort by score
        scored_products = []
        for i, product in enumerate(products_to_score):
            score = score_map.get(i, 5)
            if score >= 5:  # Keep products that score 5+ (neutral or better)
                product["vibe_score"] = score
                scored_products.append(product)

        # Sort by score descending
        scored_products.sort(key=lambda x: x.get("vibe_score", 0), reverse=True)

        # Add back any remaining unscored products at the end
        if len(products) > 30:
            scored_products.extend(products[30:])

        return scored_products

    except Exception as e:
        logger.error(f"AI re-ranking failed: {e}")
        # Return original products if re-ranking fails
        return products


def detect_budget_from_prompt(prompt: str) -> Optional[str]:
    """Detect budget hints from user prompt."""
    prompt_lower = prompt.lower()

    affordable_keywords = ['affordable', 'cheap', 'budget', 'under $50', 'under $75', 'under $100', 'inexpensive', 'low cost']
    luxury_keywords = ['luxury', 'designer', 'high-end', 'expensive', 'premium', 'splurge']

    for keyword in affordable_keywords:
        if keyword in prompt_lower:
            return "affordable"

    for keyword in luxury_keywords:
        if keyword in prompt_lower:
            return "luxury"

    return None


# Item type detection - matches frontend ProductFilters ITEM_TYPES
ITEM_TYPE_KEYWORDS = {
    'Tops': ['top', 'tops', 'blouse', 'blouses', 'shirt', 'shirts', 'tee', 'tees', 't-shirt', 't-shirts', 'tank', 'tanks', 'sweater', 'sweaters', 'hoodie', 'hoodies', 'cardigan', 'cardigans', 'pullover', 'cami', 'bodysuit'],
    'Bottoms': ['pants', 'pant', 'jeans', 'jean', 'trousers', 'shorts', 'skirt', 'skirts', 'leggings'],
    'Dresses': ['dress', 'dresses', 'gown', 'gowns', 'romper', 'rompers', 'jumpsuit', 'jumpsuits', 'maxi', 'midi'],
    'Outerwear': ['jacket', 'jackets', 'coat', 'coats', 'blazer', 'blazers', 'vest', 'vests', 'parka', 'puffer', 'trench'],
    'Shoes': ['shoe', 'shoes', 'boot', 'boots', 'sneaker', 'sneakers', 'sandal', 'sandals', 'heel', 'heels', 'flat', 'flats', 'loafer', 'loafers', 'mule', 'mules'],
    'Bags': ['bag', 'bags', 'purse', 'purses', 'tote', 'totes', 'clutch', 'backpack', 'backpacks', 'crossbody', 'handbag', 'handbags', 'satchel'],
    'Jewelry': ['necklace', 'necklaces', 'earring', 'earrings', 'bracelet', 'bracelets', 'ring', 'rings', 'jewelry', 'chain', 'chains', 'pendant'],
    'Accessories': ['scarf', 'scarves', 'hat', 'hats', 'belt', 'belts', 'sunglasses', 'watch', 'watches', 'headband']
}


def detect_item_type_from_prompt(prompt: str) -> Optional[str]:
    """Detect if user is asking for a specific item type."""
    prompt_lower = prompt.lower()

    for item_type, keywords in ITEM_TYPE_KEYWORDS.items():
        for keyword in keywords:
            # Check for whole word match (not partial)
            if f' {keyword} ' in f' {prompt_lower} ' or prompt_lower.startswith(keyword + ' ') or prompt_lower.endswith(' ' + keyword):
                return item_type

    return None


def filter_by_item_type(products: List[Dict], item_type: str) -> List[Dict]:
    """Filter products to only include specified item type."""
    if not item_type or item_type not in ITEM_TYPE_KEYWORDS:
        return products

    keywords = ITEM_TYPE_KEYWORDS[item_type]
    filtered = []

    for product in products:
        name_lower = product.get('name', '').lower()
        if any(kw in name_lower for kw in keywords):
            filtered.append(product)

    return filtered if filtered else products  # Return original if nothing matches
