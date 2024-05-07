from fastapi import HTTPException
import requests
from decouple import config
CLIENT_ID = config("GOOGLE_CLIENT_ID")
CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = config("GOOGLE_REDIRECT_URI")
def get_user_info_from_google(code: str):
    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code"
        }
    )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to authenticate with Google")

    access_token = response.json().get("access_token")

    user_info_response = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    if user_info_response.status_code != 200:
        raise HTTPException(status_code=user_info_response.status_code, detail="Failed to fetch user info from Google")
    return user_info_response.json()
