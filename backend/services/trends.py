import logging
import requests
import json
from urllib.parse import quote
from utils.trend_cache import get_cached, set_cached

logger = logging.getLogger(__name__)

# Google Trends explore URL
TRENDS_URL = "https://trends.google.com/trends/api/dailytrends"
INTEREST_URL = "https://trends.google.com/trends/api/widgetdata/multiline"


def get_trend_data(keyword: str, use_cache: bool = True) -> dict | None:
    """
    Fetch trend data for a keyword from Google Trends.
    Uses direct HTTP requests to avoid pytrends dependency issues.

    Args:
        keyword: The search term (e.g., "quiet luxury", "coquette aesthetic")
        use_cache: Whether to use cached data if available

    Returns:
        Dict with trend data or None if request fails
    """
    keyword = keyword.lower().strip()

    # Check cache first
    if use_cache:
        cached = get_cached(keyword)
        if cached is not None:
            logger.info(f"Trend cache hit for '{keyword}'")
            return cached

    logger.info(f"Fetching trend data for '{keyword}'")

    try:
        # Try using pytrends if it works
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword], timeframe='today 3-m')
        interest_df = pytrends.interest_over_time()

        if interest_df.empty:
            logger.warning(f"No trend data found for '{keyword}'")
            empty_result = {'keyword': keyword, 'data': [], 'error': 'no_data'}
            set_cached(keyword, empty_result)
            return empty_result

        data_points = interest_df[keyword].tolist()
        dates = [d.strftime('%Y-%m-%d') for d in interest_df.index]

        result = {
            'keyword': keyword,
            'data': data_points,
            'dates': dates,
            'timeframe': 'today 3-m'
        }

        set_cached(keyword, result)
        return result

    except Exception as e:
        logger.warning(f"Pytrends failed for '{keyword}': {str(e)}, using fallback")
        # Return graceful fallback - trend feature degrades but doesn't break app
        fallback_result = {'keyword': keyword, 'data': [], 'error': 'unavailable'}
        set_cached(keyword, fallback_result)
        return fallback_result


def get_trend_summary(keyword: str) -> dict:
    """
    Get a simplified trend summary for display.

    Returns:
        Dict with:
        - direction: "rising" | "falling" | "stable" | "unknown"
        - change: percentage string like "+34%" or "-12%"
        - sparkline: list of ~10 normalized values for mini chart
        - peak: when the trend peaked (e.g., "2 weeks ago", "now")
        - current: current interest value (0-100)
    """
    trend_data = get_trend_data(keyword)

    if not trend_data or not trend_data.get('data') or 'error' in trend_data:
        return {
            'keyword': keyword,
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
