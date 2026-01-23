from flask import Flask, redirect, session, make_response, jsonify, request
from dotenv import load_dotenv
from random import randint

import requests
import os
import base64
import urllib.parse

app = Flask(__name__)
app.secret_key = os.urandom(24)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5173/redirect-spotify"
SCOPE = "user-read-private user-read-email user-top-read"


@app.route("/begin-signin")
def beginSignin():
    """Redirect user to Spotify's authorization page"""
    print("[GET] /begin-signin")
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
    }
    auth_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)
    return redirect(auth_url)


@app.route("/signin")
def signin():
    """Handle Spotify's callback with authorization code"""
    print("[GET] /signin")
    code = request.args.get("code")
    error = request.args.get("error")

    if error:
        resp = make_response(jsonify({"error": error}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400

    if not code:
        resp = make_response(jsonify({"error": "No authorization code received"}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400

    # Exchange authorization code for access token
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
    token_info = response.json()

    print(token_info)

    access_token = token_info.get("access_token")

    if not access_token:
        resp = make_response(jsonify({"error": "Failed to get access token"}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400

    # Redirect to frontend with token
    resp = make_response(token_info)
    resp.headers["Access-Control-Allow-Origin"] = "*"

    return resp


@app.route("/profile")
def profile():
    print("[GET] /profile")
    token = request.args.get("token")
    
    if not token:
        resp = make_response(jsonify({"error": "No token provided"}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get("https://api.spotify.com/v1/me", headers=headers)

    print(f"Spotify API response status: {response.status_code}")
    print(f"Spotify API response: {response.text}")

    if response.status_code != 200:
        resp = make_response(
            jsonify({"error": "Failed to fetch profile"})
        )
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, response.status_code

    data = response.json()

    print(data)

    resp = make_response(data)
    resp.headers["Access-Control-Allow-Origin"] = "*"

    return resp



@app.route("/top-tracks")
def top_tracks():
    print("[GET] /top-tracks")
    token = request.args.get("token")
    
    if not token:
        resp = make_response(jsonify({"error": "No token provided"}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400
    
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        "https://api.spotify.com/v1/me/top/tracks?limit=50&time_range=long_term",
        headers=headers,
    )

    print(f"Spotify API response status: {response.status_code}")

    if response.status_code != 200:
        resp = make_response(
            jsonify({"error": "Failed to fetch top tracks"})
        )
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, response.status_code

    data = response.json()

    resp = make_response(data["items"])
    resp.headers["Access-Control-Allow-Origin"] = "*"

    return resp


@app.route("/top-artists")
def top_artists():
    print("[GET] /top-artists")
    token = request.args.get("token")
    
    if not token:
        resp = make_response(jsonify({"error": "No token provided"}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400
    
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        "https://api.spotify.com/v1/me/top/artists?limit=50&time_range=long_term",
        headers=headers,
    )

    print(f"Spotify API response status: {response.status_code}")
    print(f"Spotify API response: {response.text}")

    if response.status_code != 200:
        resp = make_response(
            jsonify({"error": "Failed to fetch top tracks"})
        )
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, response.status_code

    data = response.json()

    print(data)

    resp = make_response(jsonify(data["items"]))
    resp.headers["Access-Control-Allow-Origin"] = "*"

    return resp


@app.route("/track-details")
def track_details():
    print("[GET] /track-details")
    token = request.args.get("token")
    track_id = request.args.get("track_id")
    
    if not token:
        resp = make_response(jsonify({"error": "No token provided"}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400

    if not track_id:
        resp = make_response(jsonify({"error": "No track_id provided"}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400
    
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        f"https://api.spotify.com/v1/tracks/{track_id}",
        headers=headers,
    )

    print(f"Spotify API response status: {response.status_code}")

    if response.status_code != 200:
        resp = make_response(
            jsonify({"error": "Failed to fetch track details"})
        )
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, response.status_code

    data = response.json()

    data["compatibility_score"] = randint(0, 100) / 100 # TODO : calculer la vraie compatibilité

    resp = make_response(jsonify(data))
    resp.headers["Access-Control-Allow-Origin"] = "*"

    return resp


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
