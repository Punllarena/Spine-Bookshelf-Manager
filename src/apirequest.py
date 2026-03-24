import requests
import calendar

BASE_URL = "https://ranobedb.org/api/v0"
IMAGE_BASE_URL = "https://images.ranobedb.org/"
LIMIT = 10


def search_volume(query, page=1):
    params = {
        "q": query,
        "rl": "en",
        "limit": LIMIT,
        "page": page,
    }
    response = requests.get(f"{BASE_URL}/books", params=params)
    response.raise_for_status()
    data = response.json()
    for book in data.get("books", []):
        image = book.get("image")
        if image and image.get("filename"):
            book["image_url"] = f"{IMAGE_BASE_URL}{image['filename']}"
        else:
            book["image_url"] = "https://placehold.co/139x203"
    data["pagination"] = data.get("totalPages", 1)
    return data


def get_volume(volume_id):
    response = requests.get(f"{BASE_URL}/book/{volume_id}")
    response.raise_for_status()
    return response.json()["book"]


def get_series(series_id):
    response = requests.get(f"{BASE_URL}/series/{series_id}")
    response.raise_for_status()
    return response.json()["series"]


def get_releases(year_month):
    """Fetch English releases for a given month. year_month = 'YYYY-MM'"""
    year, month = map(int, year_month.split('-'))
    last_day = calendar.monthrange(year, month)[1]
    params = {
        "lang": "en",
        "minDate": f"{year_month}-01",
        "maxDate": f"{year_month}-{last_day:02d}",
        "limit": 100,
        "sort": "Release date asc",
    }
    response = requests.get(f"{BASE_URL}/releases", params=params)
    response.raise_for_status()
    releases = response.json().get("releases", [])
    for r in releases:
        image = r.get("image")
        r["image_url"] = f"{IMAGE_BASE_URL}{image['filename']}" if image and image.get("filename") else "https://placehold.co/139x203"
        s = str(r["release_date"])
        r["release_date_str"] = f"{s[:4]}-{s[4:6]}-{s[6:]}"
    return releases
