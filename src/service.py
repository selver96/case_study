import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sqlalchemy.orm import Session
from models import Campground as CampgroundDB, CampgroundAttributes
from urllib.parse import urlparse, parse_qs
from playwright.async_api import async_playwright

response_data = '''{
    "data": [
        {
            "id": "12345",
            "type": "location",
            "attributes": {
                "name": "Campground Name",
                "latitude": 37.95,
                "longitude": 31.60,
                "rating": 4.5,
                "price": "$$",
                "amenities": ["wifi", "electricity", "pets_allowed"],
                "description": "A beautiful campground with scenic views.",
                "max_vehicle_length": 35,
                "electric_amperage": 30,
                "air_quality": "Good",
                "drive_time": "1h 30m",
                "address": "123 Forest Road",
                "city": "Antalya",
                "state": "Antalya",
                "postal_code": "07000",
                "country": "Türkiye",
                "website": "https://campground.example.com",
                "phone_number": "+90 242 123 4567",
                "email": "info@campground.example.com",
                "operating_hours": "8 AM - 8 PM",
                "images": [
                    {"url": "https://images.example.com/campground1.jpg", "caption": "Main entrance"},
                    {"url": "https://images.example.com/campground2.jpg", "caption": "Lake view"}
                ]
            }
        }
    ],
    "meta": {
        "total": 200,
        "page": 1,
        "per_page": 500
    }
}'''


async def fetch_campgrounds():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        async def handle_request(request):
            url = request.url
            if "api/v6/locations/search-results" in url:
                parsed_url = urlparse(url)
                query_params = parse_qs(parsed_url.query)
                for key, value in query_params.items():
                    print(f"  {key} = {value}")

        async def handle_response(response):
            if "api/v6/locations/search-results" in response.url and response.status == 200:
                try:
                    data = await response.json()
                    print(response_data)
                    # save_campgrounds(response_data)
                except:
                    print("Failed to parse response JSON")

        page.on("request", handle_request)
        page.on("response", handle_response)

        await page.goto("https://thedyrt.com/search")
        await page.wait_for_timeout(5000)

        map_element = page.locator("div[id='map']")
        box = await map_element.bounding_box()
        if box:
            for x in range(int(box["x"]), int(box["x"] + box["width"]), 150):
                for y in range(int(box["y"]), int(box["y"] + box["height"]), 150):
                    await page.mouse.move(x, y)
                    await page.wait_for_timeout(300)

        await page.wait_for_timeout(5000)
        await browser.close()
    return []

# def save_campgrounds(db: Session, campgrounds: list[CampgroundDB]):
#     for camp in campgrounds:
#         existing = db.query(CampgroundDB).filter_by(id=camp.id).first()
#         data = camp.dict(by_alias=True)
#         if existing:
#             for key, value in data.items():
#                 setattr(existing, key, value)
#         else:
#             db.add(CampgroundDB(**data))
#     db.commit()


def save_campgrounds(data):
    temp = CampgroundAttributes(**data)
    print(temp)