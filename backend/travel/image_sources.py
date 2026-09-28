"""Helpers for resolving one image per destination.

The project keeps a small local cache after the first image refresh so normal
re-seeding does not repeatedly call the Wikimedia REST API. You can add a
specific URL in image_overrides.py when you want to control a particular place.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from travel.image_overrides import IMAGE_OVERRIDES

CACHE_PATH = Path(__file__).resolve().with_name("image_cache.json")
USER_AGENT = "TravelAdvisor/1.0 (local development project; destination image seeding)"


def _key(name: str, city: str, state: str, country: str) -> str:
    return "|".join((country.strip(), state.strip(), city.strip(), name.strip())).lower()


def _load_cache() -> dict[str, str]:
    try:
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}


def _save_cache(cache: dict[str, str]) -> None:
    try:
        CACHE_PATH.write_text(json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")
    except OSError:
        # A read-only checkout should not prevent seeding the database.
        pass


def _get_json(url: str) -> dict | None:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urlopen(request, timeout=12) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, ValueError, OSError):
        return None


def _summary_image(title: str) -> tuple[str, str] | None:
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + quote(title.replace(" ", "_"), safe="")
    data = _get_json(url)
    if not data:
        return None
    thumbnail = data.get("thumbnail") or {}
    source = thumbnail.get("source")
    if not source:
        original = data.get("originalimage") or {}
        source = original.get("source")
    page = ((data.get("content_urls") or {}).get("desktop") or {}).get("page")
    if source:
        return source, page or f"https://en.wikipedia.org/wiki/{quote(title.replace(' ', '_'))}"
    return None


def _search_image(query: str) -> tuple[str, str] | None:
    params = urlencode({"q": query, "limit": 5})
    url = f"https://en.wikipedia.org/w/rest.php/v1/search/page?{params}"
    data = _get_json(url)
    if not data:
        return None
    for page in data.get("pages", []):
        title = page.get("title")
        if not title:
            continue
        thumb = page.get("thumbnail") or {}
        source = thumb.get("url")
        if source:
            return source, f"https://en.wikipedia.org/wiki/{quote(title.replace(' ', '_'))}"
    return None


def fetch_wikimedia_image(name: str, city: str, state: str, country: str) -> tuple[str, str] | None:
    """Find a lead image for a destination from Wikipedia's REST API."""
    titles: list[str] = []
    for candidate in (name, city, f"{city}, {state}", f"{city}, {country}", f"{name}, {country}"):
        candidate = candidate.strip(" ,")
        if candidate and candidate not in titles:
            titles.append(candidate)

    for title in titles:
        result = _summary_image(title)
        if result:
            return result
        time.sleep(0.08)

    query = " ".join(part for part in (name, city, state, country) if part).strip()
    if query:
        return _search_image(query)
    return None


def resolve_image(name: str, city: str, state: str, country: str, fallback: str, *, refresh: bool = False) -> str:
    """Resolve a manual, cached, or live destination image, with a safe fallback."""
    key = _key(name, city, state, country)
    if key in IMAGE_OVERRIDES:
        return IMAGE_OVERRIDES[key]

    cache = _load_cache()
    if not refresh and key in cache:
        return cache[key]

    result = fetch_wikimedia_image(name, city, state, country)
    if result:
        source, _ = result
        cache[key] = source
        _save_cache(cache)
        return source
    return fallback


def resolve_image_with_source(name: str, city: str, state: str, country: str, fallback: str, *, refresh: bool = False) -> tuple[str, str | None]:
    """Return (image_url, source_page_url) for refresh/reporting."""
    key = _key(name, city, state, country)
    if key in IMAGE_OVERRIDES:
        return IMAGE_OVERRIDES[key], None

    cache = _load_cache()
    if not refresh and key in cache:
        return cache[key], None

    result = fetch_wikimedia_image(name, city, state, country)
    if result:
        source, page = result
        cache[key] = source
        _save_cache(cache)
        return source, page
    return fallback, None
