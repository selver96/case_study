import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sqlalchemy.orm import Session
from models import Campground as CampgroundDB
from urllib.parse import urlparse, parse_qs
from playwright.async_api import async_playwright

async def fetch_campgrounds():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Intercept and filter for the exact endpoint pattern
        async def handle_request(request):
            url = request.url
            if "api/v6/locations/search-results" in url:
                print("✅ API Called:", url)
                # Optional: print query parameters
                parsed_url = urlparse(url)
                query_params = parse_qs(parsed_url.query)
                print("🔍 Query Params:")
                for key, value in query_params.items():
                    print(f"  {key} = {value}")

        async def handle_response(response):
            if "api/v6/locations/search-results" in response.url and response.status == 200:
                try:
                    data = await response.json()
                    print("📦 Response contains", len(data.get("data", [])), "locations")
                except:
                    print("⚠️ Failed to parse response JSON")

        page.on("request", handle_request)
        page.on("response", handle_response)

        await page.goto("https://thedyrt.com/search")
        await page.wait_for_timeout(5000)

        # Move the mouse to trigger the API
        map_element = page.locator("div[class*='mapbox']")
        box = await map_element.bounding_box()
        if box:
            for x in range(int(box["x"]), int(box["x"] + box["width"]), 150):
                for y in range(int(box["y"]), int(box["y"] + box["height"]), 150):
                    await page.mouse.move(x, y)
                    await page.wait_for_timeout(300)

        await page.wait_for_timeout(5000)
        await browser.close()


def save_campgrounds(db: Session, campgrounds: list[CampgroundDB]):
    for camp in campgrounds:
        existing = db.query(CampgroundDB).filter_by(id=camp.id).first()
        data = camp.dict(by_alias=True)
        if existing:
            for key, value in data.items():
                setattr(existing, key, value)
        else:
            db.add(CampgroundDB(**data))
    db.commit()