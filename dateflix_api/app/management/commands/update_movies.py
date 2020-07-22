import json

import httpx
from django.core.management.base import BaseCommand

from dateflix_api import settings
from dateflix_api.app.models import Movie

NETFLIX_PROVIDER_ID = 8


"""
Para cada iteração de filmes, verificar se o filme já está no banco de dados.
Se ainda não estiver, cadastra.

Ao final, verificar se algum dos filmes que estavam no banco de dados não vieram na requisição.

"""


class Command(BaseCommand):
    help = "Command to update movies catalog from Netflix"

    def handle(self, *args, **options):
        stored_movies_dict = {m.justwatch_id: m for m in Movie.objects.all()}

        print("Updating movies list folks.")
        movies = []
        params = {
            "content_types": ["movie"],
            "providers": ["nfx"],
            "page": 0,
            "page_size": 100,
        }
        result = {"page": 1, "total_pages": None}
        updated_catalog_ids = set()
        while result["page"] != result["total_pages"]:
            params["page"] += 1
            response = httpx.get(
                f"https://apis.justwatch.com/content/titles/pt_BR/popular?body={json.dumps(params)}"
            )
            result = response.json()

            for item in result["items"]:
                updated_catalog_ids.add(item["id"])
                # If movie already stored in the database, do nothing!
                if item["id"] in stored_movies_dict:
                    continue
                movie = {
                    "title": item["title"],
                    "justwatch_id": item["id"],
                    "tmdb_id": next(
                        (
                            s["value"]
                            for s in item["scoring"]
                            if s["provider_type"] == "tmdb:id"
                        ),
                        None,
                    ),
                    "imdb_score": next(
                        (
                            s["value"]
                            for s in item["scoring"]
                            if s["provider_type"] == "imdb:score"
                        ),
                        None,
                    ),
                    "tmdb_score": next(
                        (
                            s["value"]
                            for s in item["scoring"]
                            if s["provider_type"] == "tmdb:score"
                        ),
                        None,
                    ),
                }

                # What about movie descriptions, images and Netflix URL???
                response_detail = httpx.get(
                    f"https://apis.justwatch.com/content/titles/movie/{movie['justwatch_id']}/locale/pt_BR?language=en"
                )
                result_detail = response_detail.json()
                description = result_detail.get("short_description")
                movie["netflix_url"] = next(
                    (
                        offer["urls"]["standard_web"]
                        for offer in result_detail["offers"]
                        if offer["provider_id"] == NETFLIX_PROVIDER_ID
                    ),
                    None,
                )

                movie["netflix_id"] = movie["netflix_url"].split("/")[-1]

                params_detail = {"api_key": settings.TMDB_TOKEN, "language": "pt-br"}
                response_detail = httpx.get(
                    f"https://api.themoviedb.org/3/movie/{movie['tmdb_id']}",
                    params=params_detail,
                )
                if response_detail.status_code != 200:
                    continue
                result_detail = response_detail.json()
                movie["title"] = (
                    result_detail["title"]
                    if result_detail.get("title")
                    else item["title"]
                )
                movie["description"] = (
                    result_detail["overview"]
                    if result_detail.get("overview")
                    else description
                )
                movie[
                    "image"
                ] = f"https://image.tmdb.org/t/p/w500{result_detail['poster_path']}"
                movies.append(movie)

                Movie(**movie).save()

        # Inactivate movies that left Netflix catalog
        stored_catalog_ids = set(stored_movies_dict.keys())
        diff_ids = stored_catalog_ids - updated_catalog_ids
        Movie.objects.filter(justwatch_id__in=diff_ids).update(active=False)
