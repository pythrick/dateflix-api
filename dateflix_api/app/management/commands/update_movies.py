import httpx
import json
from django.core.management.base import BaseCommand

from dateflix_api.app.models import Movie


NETFLIX_PROVIDER_ID = 8

class Command(BaseCommand):
    help = "Command to update movies catalog from Netflix"

    def handle(self, *args, **options):
        print("Updating movies list folks.")
        movies = []
        params = {
            "content_types": ["movie"],
            "providers": ["nfx"],
            "page": 0,
            "page_size": 100
        }
        result = {
            "page": 1,
            "total_pages": None
        }
        while result["page"] != result["total_pages"]:
            params["page"] += 1
            response = httpx.get(f"https://apis.justwatch.com/content/titles/pt_BR/popular?body={json.dumps(params)}")
            result = response.json()

            for item in result["items"]:
                movie = {
                    "title": item["title"],
                    "justwatch_id": item["id"],
                    "tmdb_id": next((s["value"] for s in item["scoring"] if s["provider_type"] == "tmdb:id"), None),
                    "imdb_id": next((s["value"] for s in item["scoring"] if s["provider_type"] == "imdb:score"), None),
                }
                movies.append(movie)

                # What about movie descriptions, images and Netflix URL???
                response_detail = httpx.get(
                    f"https://apis.justwatch.com/content/titles/movie/{movie['justwatch_id']}/locale/pt_BR?language=en"
                )
                result_detail = response_detail.json()

                movie["netflix_url"] = next((
                    offer["urls"]["standard_web"]
                    for offer in result_detail["offers"]
                    if offer["provider_id"] == NETFLIX_PROVIDER_ID
                ), None)
