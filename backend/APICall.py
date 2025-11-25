from flask import Flask, redirect, request, session, url_for
import requests
import os
import base64

app = Flask(__name__)
app.secret_key = os.urandom(24)

CLIENT_ID = "TON_CLIENT_ID"
CLIENT_SECRET = "TON_CLIENT_SECRET"
REDIRECT_URI = "http://127.0.0.1:5000/callback"
SCOPE = "user-read-private user-read-email"

def get_token(code):
    url = "https://accounts.spotify.com/api/token"
    
    headers = {
        "Authorization": "Basic " + base64.b64encode(
            f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
        ).decode(),
        "Content-Type": "application/x-www-form-urlencoded",
    }

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    response = requests.post(url, headers=headers, data=payload)
    return response.json()


@app.route("/")
def home():
    auth_url = (
        "https://accounts.spotify.com/authorize"
        f"?response_type=code&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}&scope={SCOPE}"
    )
    return f"<a href='{auth_url}'>Se connecter avec Spotify</a>"


@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_info = get_token(code)
    access_token = token_info.get("access_token")

    # Stocker le token en session
    session["token"] = access_token

    return redirect(url_for("profile"))


@app.route("/profile")
def profile():
    token = session.get("token")
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    data = response.json()
    
    return f"Bonjour {data['display_name']} !"
### suggerer les recommandations de musique basées sur les préférences de l'utilisateur###
@app.route("/recoSpotify")
def recommendations(limit,country,music_type,track_list):
    token = session.get("token")
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "limit": limit,
        "market": country,
        "seed_genres": music_type,
        "seed_tracks": track_list
        }
    response = requests.get("https://api.spotify.com/v1/recommendations", headers=headers, params=params)
    reco= response.json()
    return reco


if __name__ == "__main__":
    app.run(debug=True)
