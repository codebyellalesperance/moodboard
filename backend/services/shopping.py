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
    Enhance search queries with trending modifier (simplified).
    Brand-specific queries are now handled separately.
    """
    if not queries:
        return queries
    enhanced = []
    for i, query in enumerate(queries[:6]):
        if i < 2:
            enhanced.append(f"trending {query}")
        else:
            enhanced.append(query)
    return enhanced


def create_brand_queries(
    target_brands: Dict,
    key_pieces: List[str],
    budget: Optional[str] = None
) -> List[str]:
    """
    Create brand-specific search queries based on extracted target brands.

    Args:
        target_brands: Dict with 'aspirational', 'contemporary', 'accessible' lists
        key_pieces: List of key pieces from the vibe profile
        budget: User's budget preference (affects which brands to prioritize)

    Returns:
        List of brand-specific search queries
    """
    brand_queries = []

    # Get brands from each tier
    aspirational = target_brands.get('aspirational', [])[:2]
    contemporary = target_brands.get('contemporary', [])[:2]
    accessible = target_brands.get('accessible', [])[:2]

    # Select which tiers to use based on budget
    if budget == "affordable":
        # Focus on accessible, some contemporary
        brands_to_use = accessible + contemporary[:1]
    elif budget == "luxury":
        # Focus on aspirational, some contemporary
        brands_to_use = aspirational + contemporary[:1]
    else:
        # Mix of all tiers (default)
        brands_to_use = contemporary + accessible[:1] + aspirational[:1]

    # Get a few key pieces to pair with brands
    pieces_for_brands = key_pieces[:3] if key_pieces else ["clothing", "accessories"]

    # Create brand + piece queries
    for brand in brands_to_use:
        if brand:
            # Pick a key piece for this brand
            piece = pieces_for_brands[len(brand_queries) % len(pieces_for_brands)]
            brand_queries.append(f"{brand} {piece} women")

    # Also add some pure brand queries for discovery
    for brand in brands_to_use[:2]:
        if brand:
            brand_queries.append(f"{brand} new arrivals women")

    return brand_queries


def search_all_queries(
    search_queries: List[str],
    max_products: int = 20,
    budget: Optional[str] = None,
    vibe_profile: Optional[Dict] = None
) -> List[Dict]:
    """
    Search multiple queries, filter, re-rank with AI, and return best matches.
    Now includes brand-specific queries from the vibe profile.
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

    # Build query list: enhanced base queries + brand-specific queries
    base_queries = enhance_queries_with_modifiers(search_queries[:5])

    # Add brand-specific queries if we have target brands
    brand_queries = []
    if vibe_profile:
        target_brands = vibe_profile.get('target_brands', {})
        key_pieces = vibe_profile.get('key_pieces', [])
        if target_brands:
            brand_queries = create_brand_queries(target_brands, key_pieces, budget)
            logger.info(f"Brand queries: {brand_queries}")

    # Combine: 5 base queries + up to 4 brand queries = max 9 parallel searches
    queries_to_use = base_queries + brand_queries[:4]
    logger.info(f"Total queries ({len(queries_to_use)}): {queries_to_use}")
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

    with ThreadPoolExecutor(max_workers=9) as executor:
        futures = {executor.submit(fetch_query, q): q for q in queries_to_use}
        for future in as_completed(futures):
            query = futures[future]
            products = future.result()
            is_brand_query = query in brand_queries
            for product in products:
                product_key = product["id"] + product.get("product_url", "")
                if product_key not in seen_ids:
                    seen_ids.add(product_key)
                    # Add brand score for curated/editorial brand boosting
                    product["brand_score"] = get_brand_score(product.get("brand", ""))
                    # Mark products from brand queries for potential boost
                    if is_brand_query:
                        product["from_brand_query"] = True
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

    # Sort: by vibe score (highest first), then brand query boost, then brand score, then on-sale, then by price
    trusted_products.sort(key=lambda x: (
        -x.get("vibe_score", 5),          # Higher vibe scores first
        -int(x.get("from_brand_query", False)),  # Products from target brand queries
        -x.get("brand_score", 0),         # Higher brand scores third
        not x.get("on_sale", False),      # Sale items fourth
        x.get("price", 0)                 # Lower prices last
    ))

    # Apply category diversity to ensure mix of tops, bottoms, shoes, accessories, etc.
    diversified = ensure_category_diversity(
        trusted_products,
        max_products=max_products,
        min_per_category=1,  # Try to include at least 1 from each category
        max_per_category=4   # Don't let any single category dominate
    )
    logger.info(f"After diversity filter: {len(diversified)} products")

    # Build bench of alternative products for coherence swaps
    diversified_ids = {p.get('id', '') + p.get('product_url', '') for p in diversified}
    bench_products = [
        p for p in trusted_products
        if (p.get('id', '') + p.get('product_url', '')) not in diversified_ids
        and p.get('vibe_score', 0) >= 5  # Only consider decent alternatives
    ][:15]  # Keep top 15 alternatives

    # Apply outfit coherence scoring if we have a vibe profile
    if vibe_profile and len(diversified) >= 5:
        diversified = score_outfit_coherence(
            selected_products=diversified,
            bench_products=bench_products,
            vibe_profile=vibe_profile,
            max_swaps=3  # Allow up to 3 items to be swapped for better coherence
        )
        logger.info(f"After coherence scoring: {len(diversified)} products")

    return diversified


def rerank_products_with_ai(products: List[Dict], vibe_profile: Dict) -> List[Dict]:
    """
    Use GPT-4o with vision to score products based on how well they VISUALLY match the vibe.
    Analyzes actual product images, not just names/brands.
    Returns products with score >= 6, sorted by score descending.
    """
    if not products:
        return []

    # Limit to 15 products for visual analysis (API handles ~15-20 images well)
    # We'll score the rest with text-only as fallback
    products_for_visual = products[:15]
    products_text_only = products[15:30] if len(products) > 15 else []

    # Build brand guidance
    curated_sample = ", ".join(list(CURATED_BRANDS)[:8])
    editorial_sample = ", ".join(list(EDITORIAL_BRANDS)[:8])

    # Extract color palette for visual matching
    colors = vibe_profile.get('color_palette', [])
    color_names = [c.get('name', '') for c in colors[:5]]

    # Build the visual prompt
    visual_prompt = f"""You are a fashion stylist curating products for a client. Look at each product image and score how well it VISUALLY matches this aesthetic.

AESTHETIC: {vibe_profile.get('name', 'Unknown')}
MOOD: {vibe_profile.get('mood', '')}
COLOR PALETTE: {', '.join(color_names)}
KEY PIECES: {', '.join(vibe_profile.get('key_pieces', []))}
TEXTURES TO LOOK FOR: {', '.join(vibe_profile.get('textures', []))}
AVOID: {', '.join(vibe_profile.get('avoid', []))}

BRAND PREFERENCES (give +1 boost):
- Premium: {curated_sample}
- Editorial: {editorial_sample}

I'm showing you {len(products_for_visual)} product images. For each image (in order), score 1-10:
- 9-10: Perfect visual match - colors, silhouette, texture all align with the aesthetic
- 7-8: Strong match - looks like it belongs in this wardrobe
- 5-6: Decent fit - could work but not ideal
- 3-4: Weak match - wrong colors, style, or vibe
- 1-2: Completely wrong aesthetic

VISUAL SCORING CRITERIA:
- Does the COLOR match the palette? (Most important)
- Does the SILHOUETTE match the aesthetic's energy?
- Does the TEXTURE/MATERIAL look right?
- Is it a statement piece or interesting detail that elevates the look?
- Would this photograph well in a mood board with the aesthetic?

Product details for context:
"""

    # Add product metadata
    for i, p in enumerate(products_for_visual):
        visual_prompt += f"\nImage {i+1}: {p.get('name', 'Unknown')} by {p.get('brand', 'Unknown')} - ${p.get('price', 0)}"

    visual_prompt += "\n\nReturn ONLY a JSON array with scores: [{\"index\": 1, \"score\": 7}, {\"index\": 2, \"score\": 4}, ...]"

    # Build multimodal content with images
    content = [{"type": "text", "text": visual_prompt}]

    # Add product images
    for p in products_for_visual:
        image_url = p.get("image_url", "")
        if image_url:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": image_url,
                    "detail": "low"  # Use low detail for cost efficiency
                }
            })

    try:
        # Use GPT-4o for vision capability
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": content}],
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

        # Build score map (GPT returns 1-indexed, convert to 0-indexed)
        score_map = {}
        for item in scores:
            idx = item.get("index", 0)
            # Handle both 0-indexed and 1-indexed responses
            if idx > 0 and idx <= len(products_for_visual):
                score_map[idx - 1] = item["score"]
            elif idx >= 0 and idx < len(products_for_visual):
                score_map[idx] = item["score"]

        # Apply scores to visually analyzed products
        scored_products = []
        for i, product in enumerate(products_for_visual):
            score = score_map.get(i, 5)
            if score >= 6:  # Raised threshold for better quality
                product["vibe_score"] = score
                product["visual_scored"] = True
                scored_products.append(product)

        logger.info(f"Visual re-ranking: {len(scored_products)}/{len(products_for_visual)} products scored 6+")

        # Score remaining products with text-only (fallback for products 16-30)
        if products_text_only:
            text_scored = _rerank_text_only(products_text_only, vibe_profile)
            scored_products.extend(text_scored)

        # Sort by score descending
        scored_products.sort(key=lambda x: x.get("vibe_score", 0), reverse=True)

        # Add back any remaining unscored products at the end (31+)
        if len(products) > 30:
            for p in products[30:]:
                p["vibe_score"] = 4  # Default low score for unanalyzed
            scored_products.extend(products[30:])

        return scored_products

    except Exception as e:
        logger.error(f"Visual re-ranking failed: {e}")
        # Fall back to text-only ranking
        return _rerank_text_only(products[:30], vibe_profile)


def _rerank_text_only(products: List[Dict], vibe_profile: Dict) -> List[Dict]:
    """
    Fallback text-only re-ranking when visual analysis isn't possible.
    Uses product names and brands only.
    """
    if not products:
        return []

    product_list = []
    for i, p in enumerate(products):
        product_list.append({
            "index": i,
            "name": p.get("name", ""),
            "brand": p.get("brand", ""),
            "price": p.get("price", 0)
        })

    prompt = f"""Score how well each product fits the "{vibe_profile.get('name', 'Unknown')}" aesthetic.
Mood: {vibe_profile.get('mood', '')}
Key pieces: {', '.join(vibe_profile.get('key_pieces', []))}

Products:
{json.dumps(product_list, indent=2)}

Score 1-10. Return ONLY JSON: [{{"index": 0, "score": 7}}]"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.3
        )

        response_text = response.choices[0].message.content.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]

        scores = json.loads(response_text.strip())
        score_map = {item["index"]: item["score"] for item in scores}

        scored = []
        for i, product in enumerate(products):
            score = score_map.get(i, 5)
            if score >= 6:
                product["vibe_score"] = score
                product["visual_scored"] = False
                scored.append(product)

        return scored

    except Exception as e:
        logger.error(f"Text-only re-ranking failed: {e}")
        # Return products with default score
        for p in products:
            p["vibe_score"] = 5
        return products


def score_outfit_coherence(
    selected_products: List[Dict],
    bench_products: List[Dict],
    vibe_profile: Dict,
    max_swaps: int = 3
) -> List[Dict]:
    """
    Evaluate how well selected products work together as a cohesive outfit/wardrobe.
    Identifies outliers and swaps them with better-fitting alternatives from the bench.

    Args:
        selected_products: The current selection (typically 20 items)
        bench_products: Alternative products that didn't make the initial cut
        vibe_profile: The aesthetic profile for context
        max_swaps: Maximum number of items to swap out

    Returns:
        Refined list with better outfit coherence
    """
    if not selected_products or len(selected_products) < 5:
        return selected_products

    # Limit to 15 products for visual analysis
    products_to_analyze = selected_products[:15]

    # Build the coherence prompt
    coherence_prompt = f"""You are a fashion stylist reviewing a curated collection for a client.

AESTHETIC: {vibe_profile.get('name', 'Unknown')}
MOOD: {vibe_profile.get('mood', '')}
COLOR PALETTE: {', '.join([c.get('name', '') for c in vibe_profile.get('color_palette', [])[:5]])}

I'm showing you {len(products_to_analyze)} products that have been selected for this aesthetic.

EVALUATE OUTFIT COHERENCE:
1. Do these items work together as a cohesive wardrobe?
2. Are there any OUTLIERS that don't fit with the rest?
3. Consider: color harmony, style consistency, occasion compatibility

For each product (in order), respond with:
- "keep" if it fits well with the collection
- "swap" if it's an outlier that doesn't belong

IMPORTANT: Only mark items as "swap" if they truly clash with the overall aesthetic.
We want a cohesive collection, but some variety is good.
Maximum {max_swaps} swaps allowed.

Product details:
"""

    # Add product metadata
    for i, p in enumerate(products_to_analyze):
        cat = p.get('_category', 'Unknown')
        coherence_prompt += f"\nImage {i+1}: [{cat}] {p.get('name', 'Unknown')} - ${p.get('price', 0)}"

    coherence_prompt += f"""

Return ONLY a JSON array with your decisions:
[{{"index": 1, "decision": "keep", "reason": "matches color palette"}}, {{"index": 2, "decision": "swap", "reason": "too casual for the aesthetic"}}]

Every item needs a decision. Use 1-indexed positions matching the images."""

    # Build multimodal content with images
    content = [{"type": "text", "text": coherence_prompt}]

    for p in products_to_analyze:
        image_url = p.get("image_url", "")
        if image_url:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": image_url,
                    "detail": "low"
                }
            })

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": content}],
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

        decisions = json.loads(response_text)

        # Find items to swap (1-indexed from GPT)
        swap_indices = []
        for item in decisions:
            idx = item.get("index", 0)
            if item.get("decision") == "swap" and len(swap_indices) < max_swaps:
                # Convert to 0-indexed
                if 1 <= idx <= len(products_to_analyze):
                    swap_indices.append(idx - 1)
                    logger.info(f"Coherence swap: Item {idx} ({products_to_analyze[idx-1].get('name', '')[:30]}) - {item.get('reason', 'no reason')}")

        if not swap_indices:
            logger.info("Coherence check: All items fit well together")
            return selected_products

        # Perform swaps with bench products
        result = selected_products.copy()
        bench_idx = 0

        for swap_idx in swap_indices:
            if swap_idx < len(result) and bench_idx < len(bench_products):
                # Get the category of the item being swapped
                swap_category = result[swap_idx].get('_category', 'Other')

                # Try to find a bench product in the same category
                replacement = None
                for bp in bench_products[bench_idx:]:
                    bp_category = detect_product_category(bp.get('name', ''))
                    if bp_category == swap_category:
                        replacement = bp
                        bench_products.remove(bp)
                        break

                # If no same-category replacement, just take next bench item
                if not replacement and bench_idx < len(bench_products):
                    replacement = bench_products[bench_idx]
                    bench_idx += 1

                if replacement:
                    replacement['_swapped_in'] = True
                    replacement['_replaced'] = result[swap_idx].get('name', '')[:30]
                    result[swap_idx] = replacement
                    logger.info(f"Swapped in: {replacement.get('name', '')[:30]}")

        logger.info(f"Coherence scoring: {len(swap_indices)} items swapped for better fit")
        return result

    except Exception as e:
        logger.error(f"Outfit coherence scoring failed: {e}")
        return selected_products


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


def detect_product_category(product_name: str) -> str:
    """
    Detect the category of a product based on its name.
    Returns category name or 'Other' if no match found.
    """
    name_lower = product_name.lower()

    for category, keywords in ITEM_TYPE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in name_lower:
                return category

    return 'Other'


def ensure_category_diversity(
    products: List[Dict],
    max_products: int = 20,
    min_per_category: int = 1,
    max_per_category: int = 4
) -> List[Dict]:
    """
    Ensure diverse category representation in results.

    Strategy:
    1. Group products by category
    2. Take top items from each category (sorted by vibe_score)
    3. Round-robin select to ensure variety
    4. Fill remaining slots with highest-scored items

    Args:
        products: List of products (should already be scored)
        max_products: Maximum number of products to return
        min_per_category: Try to include at least this many from each category
        max_per_category: Don't include more than this many from any one category

    Returns:
        Diversified list of products
    """
    if len(products) <= max_products:
        return products

    # Group by category
    by_category: Dict[str, List[Dict]] = {}
    for p in products:
        cat = detect_product_category(p.get('name', ''))
        p['_category'] = cat  # Store for debugging
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(p)

    # Sort each category by vibe_score (descending)
    for cat in by_category:
        by_category[cat].sort(key=lambda x: x.get('vibe_score', 0), reverse=True)

    logger.info(f"Category distribution before diversity: {{{', '.join(f'{k}: {len(v)}' for k, v in by_category.items())}}}")

    # Priority categories (clothing essentials first, then accessories)
    priority_order = ['Tops', 'Bottoms', 'Dresses', 'Outerwear', 'Shoes', 'Bags', 'Jewelry', 'Accessories', 'Other']

    diversified = []
    category_counts = {cat: 0 for cat in priority_order}
    used_ids = set()

    # Round 1: Take min_per_category from each category that has items
    for cat in priority_order:
        if cat in by_category:
            for p in by_category[cat][:min_per_category]:
                pid = p.get('id', '') + p.get('product_url', '')
                if pid not in used_ids and len(diversified) < max_products:
                    diversified.append(p)
                    used_ids.add(pid)
                    category_counts[cat] += 1

    # Round 2: Round-robin fill up to max_per_category
    slots_remaining = max_products - len(diversified)
    round_robin_idx = 0

    while slots_remaining > 0:
        added_this_round = False
        for cat in priority_order:
            if cat not in by_category:
                continue
            if category_counts[cat] >= max_per_category:
                continue

            # Find next unused product in this category
            for p in by_category[cat]:
                pid = p.get('id', '') + p.get('product_url', '')
                if pid not in used_ids:
                    diversified.append(p)
                    used_ids.add(pid)
                    category_counts[cat] += 1
                    slots_remaining -= 1
                    added_this_round = True
                    break

            if slots_remaining <= 0:
                break

        # If we couldn't add anything in a full round, break to avoid infinite loop
        if not added_this_round:
            break
        round_robin_idx += 1

    # Round 3: If we still have slots, fill with highest-scored remaining products
    if len(diversified) < max_products:
        remaining = [p for p in products if (p.get('id', '') + p.get('product_url', '')) not in used_ids]
        remaining.sort(key=lambda x: x.get('vibe_score', 0), reverse=True)
        for p in remaining:
            if len(diversified) >= max_products:
                break
            diversified.append(p)

    # Final sort by vibe_score to present best items first
    diversified.sort(key=lambda x: x.get('vibe_score', 0), reverse=True)

    logger.info(f"Category distribution after diversity: {{{', '.join(f'{k}: {v}' for k, v in category_counts.items() if v > 0)}}}")

    return diversified


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
