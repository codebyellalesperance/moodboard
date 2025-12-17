import logging
import requests
import json
import re
from urllib.parse import quote

logger = logging.getLogger(__name__)

# Google Trends explore URL
TRENDS_URL = "https://trends.google.com/trends/api/dailytrends"
INTEREST_URL = "https://trends.google.com/trends/api/widgetdata/multiline"

# Known fashion/style terms that work well with Google Trends
TRENDABLE_TERMS = {
    # Core aesthetics
    "minimalist", "maximalist", "boho", "bohemian", "preppy", "classic",
    "romantic", "edgy", "sporty", "glamorous", "artsy", "grunge", "vintage",
    # Trending aesthetics
    "quiet luxury", "old money", "coastal grandmother", "dark academia",
    "light academia", "cottagecore", "coquette", "clean girl", "mob wife",
    "tomato girl", "strawberry girl", "vanilla girl", "latte makeup",
    "streetwear", "y2k", "90s fashion", "00s fashion",
    # Style descriptors
    "capsule wardrobe", "french girl style", "scandinavian style",
    "italian style", "coastal style", "resort wear", "athleisure",
    # Seasonal
    "summer fashion", "fall fashion", "winter fashion", "spring fashion",
}

# Words to strip from vibe names (not useful for trends)
STRIP_WORDS = {
    "the", "a", "an", "and", "or", "of", "for", "with", "in", "on",
    "chic", "vibes", "vibe", "aesthetic", "style", "look", "inspired",
    "meets", "new", "modern", "classic", "effortless"
}


def get_trend_data(keyword: str, use_cache: bool = True) -> dict | None:
    """
    Fetch trend data for a keyword from Google Trends.
    Uses direct HTTP requests to avoid pytrends dependency issues.

    NOTE: This function is currently unused. Cache functionality disabled.

    Args:
        keyword: The search term (e.g., "quiet luxury", "coquette aesthetic")
        use_cache: Whether to use cached data if available (currently ignored)

    Returns:
        Dict with trend data or None if request fails
    """
    keyword = keyword.lower().strip()

    # Cache functionality removed - trend_cache.py moved to _archive
    logger.info(f"Fetching trend data for '{keyword}'")

    try:
        # Try using pytrends if it works
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword], timeframe='today 3-m')
        interest_df = pytrends.interest_over_time()

        if interest_df.empty:
            logger.warning(f"No trend data found for '{keyword}'")
            return {'keyword': keyword, 'data': [], 'error': 'no_data'}

        data_points = interest_df[keyword].tolist()
        dates = [d.strftime('%Y-%m-%d') for d in interest_df.index]

        return {
            'keyword': keyword,
            'data': data_points,
            'dates': dates,
            'timeframe': 'today 3-m'
        }

    except Exception as e:
        logger.warning(f"Pytrends failed for '{keyword}': {str(e)}, using fallback")
        # Return graceful fallback - trend feature degrades but doesn't break app
        return {'keyword': keyword, 'data': [], 'error': 'unavailable'}


def extract_trendable_keywords(vibe_name: str, style_archetype: dict = None) -> list:
    """
    Extract searchable trend keywords from a vibe name and style archetype.

    Args:
        vibe_name: The aesthetic name (e.g., "New England Summer Chic")
        style_archetype: Optional dict with 'primary' and 'secondary' archetypes

    Returns:
        List of keywords to try, in order of preference
    """
    keywords = []
    vibe_lower = vibe_name.lower()

    # 1. Check if vibe name matches any known trendable term directly
    for term in TRENDABLE_TERMS:
        if term in vibe_lower:
            keywords.append(term)

    # 2. Use style archetype if provided (most reliable)
    if style_archetype:
        primary = style_archetype.get('primary', '').lower()
        secondary = style_archetype.get('secondary', '')

        if primary:
            # Try archetype + style/aesthetic
            keywords.append(f"{primary} style")
            keywords.append(f"{primary} aesthetic")
            keywords.append(primary)

        if secondary:
            secondary = secondary.lower()
            keywords.append(f"{secondary} style")

    # 3. Extract meaningful words from vibe name
    words = re.findall(r'\b[a-z]+\b', vibe_lower)
    meaningful_words = [w for w in words if w not in STRIP_WORDS and len(w) > 3]

    # Try combinations of meaningful words + "style"/"fashion"
    if meaningful_words:
        # First meaningful word + style
        keywords.append(f"{meaningful_words[0]} style")
        keywords.append(f"{meaningful_words[0]} fashion")

        # If there are location/descriptor words, try them
        for word in meaningful_words:
            if word in {"coastal", "french", "italian", "scandinavian", "european",
                       "american", "british", "japanese", "korean", "summer", "winter",
                       "fall", "spring", "resort", "beach", "city", "country"}:
                keywords.append(f"{word} style")

    # 4. Generic fallbacks
    keywords.extend(["fashion trends", "style trends"])

    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            unique_keywords.append(kw)

    return unique_keywords


def get_trend_summary(keyword: str, style_archetype: dict = None) -> dict:
    """
    Get a simplified trend summary for display.

    Args:
        keyword: The vibe name to search trends for
        style_archetype: Optional style archetype dict for smarter keyword extraction

    Returns:
        Dict with:
        - direction: "rising" | "falling" | "stable" | "unknown"
        - change: percentage string like "+34%" or "-12%"
        - sparkline: list of ~10 normalized values for mini chart
        - peak: when the trend peaked (e.g., "2 weeks ago", "now")
        - current: current interest value (0-100)
        - searched_term: the actual term that returned data
    """
    # Extract multiple keywords to try
    keywords_to_try = extract_trendable_keywords(keyword, style_archetype)
    logger.info(f"Trend keywords to try: {keywords_to_try[:5]}")

    # Try each keyword until we get data
    trend_data = None
    searched_term = keyword

    for kw in keywords_to_try[:5]:  # Try up to 5 keywords
        trend_data = get_trend_data(kw)
        if trend_data and trend_data.get('data') and 'error' not in trend_data:
            searched_term = kw
            logger.info(f"Found trend data using: '{kw}'")
            break

    if not trend_data or not trend_data.get('data') or 'error' in trend_data:
        logger.warning(f"No trend data found for any keyword variant of '{keyword}'")
        return {
            'keyword': keyword,
            'searched_term': None,
            'direction': 'unknown',
            'change': None,
            'sparkline': [],
            'peak': None,
            'current': None
        }

    data = trend_data['data']
    dates = trend_data.get('dates', [])

    if len(data) < 2:
        return {
            'keyword': keyword,
            'direction': 'unknown',
            'change': None,
            'sparkline': data,
            'peak': None,
            'current': data[0] if data else None
        }

    # Calculate metrics
    current = data[-1]
    previous = data[0]
    max_value = max(data)
    max_index = data.index(max_value)

    # Calculate percentage change
    if previous > 0:
        change_pct = ((current - previous) / previous) * 100
    else:
        change_pct = 100 if current > 0 else 0

    # Determine direction
    if change_pct > 15:
        direction = 'rising'
    elif change_pct < -15:
        direction = 'falling'
    else:
        direction = 'stable'

    # Format change string
    if change_pct >= 0:
        change_str = f"+{int(change_pct)}%"
    else:
        change_str = f"{int(change_pct)}%"

    # Create sparkline (normalize to ~10 points)
    if len(data) > 10:
        step = len(data) // 10
        sparkline = [data[i] for i in range(0, len(data), step)][:10]
    else:
        sparkline = data

    # Determine peak timing
    if max_index == len(data) - 1:
        peak = 'now'
    else:
        weeks_ago = (len(data) - 1 - max_index) // 7
        if weeks_ago == 0:
            peak = 'this week'
        elif weeks_ago == 1:
            peak = '1 week ago'
        elif weeks_ago < 4:
            peak = f'{weeks_ago} weeks ago'
        else:
            months_ago = weeks_ago // 4
            if months_ago == 1:
                peak = '1 month ago'
            else:
                peak = f'{months_ago} months ago'

    return {
        'keyword': keyword,
        'searched_term': searched_term,
        'direction': direction,
        'change': change_str,
        'sparkline': sparkline,
        'peak': peak,
        'current': current
    }


def get_related_queries(keyword: str) -> list:
    """
    Get related rising queries for a keyword.
    Useful for suggesting related aesthetics.
    """
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword], timeframe=TIMEFRAME_3M)
        related = pytrends.related_queries()

        if keyword in related and related[keyword]['rising'] is not None:
            rising = related[keyword]['rising']
            return rising['query'].tolist()[:5]
    except Exception as e:
        logger.error(f"Error fetching related queries: {str(e)}")

    return []
