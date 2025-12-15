from flask import Flask, redirect, session
import requests
import os
import base64
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.urandom(24)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5000/signin"
SCOPE = "user-read-private user-read-email"

def get_token():
    print("get token")
    url = "https://accounts.spotify.com/api/token"
    
    headers = {
        "Authorization": "Basic " + base64.b64encode(
            f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
        ).decode(),
        "Content-Type": "application/x-www-form-urlencoded",
    }

    payload = {
        "grant_type": "client_credentials",
        "redirect_uri": REDIRECT_URI,
    }

    response = requests.post(url, headers=headers, data=payload)
    return response.json()


@app.route("/signin")
def signin():
    token_info = get_token()
    access_token = token_info.get("access_token")

    # Stocker le token en session
    session["token"] = access_token

    return redirect(f"http://localhost:5173/redirect-spotify?token={access_token}")


@app.route("/profile")
def profile():
    token = session.get("token")
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    data = response.json()

    return f"Bonjour {data['display_name']} !"


# Pour les tests :
@app.route("/")
def home():
    auth_url = (
        "https://accounts.spotify.com/authorize"
        f"?response_type=code&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}&scope={SCOPE}"
    )
    return f"<a href='{auth_url}'>Se connecter avec Spotify</a>"



if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)
