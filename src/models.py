from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl



class CampgroundLinks(BaseModel):

    self: HttpUrl


class Campground(BaseModel):
    """
    Base pydantic model, these are the required fields for parsing.
    """
    id: str
    type: str
    links: CampgroundLinks
    name: str
    latitude: float
    longitude: float
    region_name: str = Field(..., alias="region-name")
    administrative_area: Optional[str] = Field(None, alias="administrative-area")
    nearest_city_name: Optional[str] = Field(None, alias="nearest-city-name")
    accommodation_type_names: List[str] = Field([], alias="accommodation-type-names")
    bookable: bool = False
    camper_types: List[str] = Field([], alias="camper-types")
    operator: Optional[str] = None
    photo_url: Optional[HttpUrl] = Field(None, alias="photo-url")
    photo_urls: List[HttpUrl] = Field([], alias="photo-urls")
    photos_count: int = Field(0, alias="photos-count")
    rating: Optional[float] = None
    reviews_count: int = Field(0, alias="reviews-count")
    slug: Optional[str] = None
    price_low: Optional[float] = Field(None, alias="price-low")
    price_high: Optional[float] = Field(None, alias="price-high")
    availability_updated_at: Optional[datetime] = Field(
        None, alias="availability-updated-at"
    )
    # address: Optinal[str] = "" For bonus point



class Image(BaseModel):
    url: str
    caption: str


class CampgroundAttributes(BaseModel):
    name: str
    latitude: float
    longitude: float
    rating: Optional[float] = None
    price: Optional[str] = None
    amenities: List[str]
    description: Optional[str] = None
    max_vehicle_length: Optional[int] = None
    electric_amperage: Optional[int] = None
    air_quality: Optional[str] = None
    drive_time: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    website: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    operating_hours: Optional[str] = None
    images: Optional[List[Image]] = None


class CampgroundData(BaseModel):
    id: str
    type: str
    attributes: CampgroundAttributes


class Meta(BaseModel):
    total: int
    page: int
    per_page: int


class CampgroundResponse(BaseModel):
    data: List[CampgroundData]
    meta: Meta
