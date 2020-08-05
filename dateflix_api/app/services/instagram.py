from typing import List

import httpx

from dateflix_api import settings


def authenticate(code: str, redirect_uri: str):
    url = "https://api.instagram.com/oauth/access_token"
    params = {
        "client_id": settings.INSTAGRAM_CLIENT_ID,  # type: ignore
        "client_secret": settings.INSTAGRAM_CLIENT_SECRET,  # type: ignore
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
        "code": code,
    }
    response = httpx.post(url, data=params)
    response.json()
    response.raise_for_status()
    return response.json()


def get_profile(access_token: str):
    url = "https://graph.instagram.com/me"
    params = {"fields": "id,username,media", "access_token": access_token}
    response = httpx.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data


def get_pictures(
    access_token: str, images_ids: List[str], media_limit: int = 5
) -> List[str]:
    pictures: List[str] = []
    for id in images_ids:
        if len(pictures) == media_limit:
            break
        image_url = f"https://graph.instagram.com/{id}"
        image_params = {
            "fields": "id,media_type,media_url,username,timestamp",
            "access_token": access_token,
        }
        image_response = httpx.get(image_url, params=image_params)
        image_data = image_response.json()
        if image_data["media_type"] == "IMAGE":
            pictures.append(image_data["media_url"])
    return pictures


"https://scontent.cdninstagram.com/v/t51.29350-15/115164885_214224233240807_3791849697703167121_n.jpg?_nc_cat=109&_nc_sid=8ae9d6&_nc_ohc=QK-JdqqZO-EAX81nO8H&_nc_ht=scontent.cdninstagram.com&oh=6ccd666660c9c321b3475f50e2aced2d&oe=5F47BB5B"
