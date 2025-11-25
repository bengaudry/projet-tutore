from flask import Flask, redirect, request, session, url_for, jsonify
import requests
import base64
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# -------------------
# CONFIG SPOTIFY
# -------------------
CLIENT_ID = "TON_CLIENT_ID"
CLIENT_SECRET = "TON_CLIENT_SECRET"
REDIRECT_URI = "http://127.0.0.1:5000/callback"
SCOPE = "user-read-private user-read-email playlist-read-private"


# -------------------------
# 1) PAGE D’ACCUEIL
# -------------------------
@app.route("/")
def index():
    auth_url = (
        "https://accounts.spotify.com/authorize"
        f"?response_type=code&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}&scope={SCOPE}"
    )
    return f"<a href='{auth_url}'>Connexion Spotify</a>"


# -------------------------
# 2) CALLBACK SPOTIFY
#    (Spotify redirige ici)
# -------------------------
@app.route("/callback")
def callback():
    code = request.args.get("code")

    # Préparer la requête token
    token_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(
            f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
        ).decode(),
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    # Requête pour obtenir le token
    response = requests.post(token_url, headers=headers, data=data)
    token_info = response.json()

    # Stocker le token en session
    session["token"] = token_info.get("access_token")

    return redirect(url_for("me"))


# -------------------------
# 3) PROFIL UTILISATEUR
# -------------------------
@app.route("/me")
def me():
    token = session.get("token")
    headers = {"Authorization": f"Bearer {token}"}

    r = requests.get("https://api.spotify.com/v1/me", headers=headers)

    return jsonify(r.json())


# -------------------------
# 4) PLAYLISTS UTILISATEUR
# -------------------------
@app.route("/playlists")
def playlists():
    token = session.get("token")
    headers = {"Authorization": f"Bearer {token}"}

    r = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)

    return jsonify(r.json())


if __name__ == "__main__":
    app.run(debug=True)
