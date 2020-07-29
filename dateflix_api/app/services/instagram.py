import httpx

from dateflix_api import settings


def authenticate(code: str):
    url = "https://api.instagram.com/oauth/access_token"
    params = {
        "client_id": settings.INSTAGRAM_CLIENT_ID,  # noqa
        "client_secret": settings.INSTAGRAM_CLIENT_SECRET,  # noqa
        "grant_type": "authorization_code",
        "redirect_uri": "https://dateflix-teste.free.beeceptor.com/",
        "code": code,
    }
    response = httpx.post(url, data=params)
    response.raise_for_status()
    return response.json()
