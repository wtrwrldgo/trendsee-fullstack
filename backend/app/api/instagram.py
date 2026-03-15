import re
import httpx
from fastapi import APIRouter

router = APIRouter()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


async def scrape_reel_stats(reel_id: str) -> dict:
    """Fetch the embed page of a reel and extract likes count from the HTML."""
    url = f"https://www.instagram.com/reel/{reel_id}/embed/"
    async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
        resp = await client.get(url, headers=HEADERS)
        html = resp.text

    likes = 0
    # Pattern: >486 likes< or >4,239 likes<
    m = re.search(r">([0-9,]+)\s+likes?<", html)
    if m:
        likes = int(m.group(1).replace(",", ""))

    comments = 0
    # Pattern: View all 123 comments
    m = re.search(r"View all\s+([0-9,]+)\s+comments?", html)
    if m:
        comments = int(m.group(1).replace(",", ""))

    return {"likes": likes, "comments": comments}


@router.get("/reel/{reel_id}/stats")
async def get_reel_stats(reel_id: str):
    stats = await scrape_reel_stats(reel_id)
    return stats
