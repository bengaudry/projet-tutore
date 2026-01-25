from flask import Flask, redirect, make_response, jsonify, request
from dotenv import load_dotenv
from track_compatibility import compute_track_compatibility
from database import store_user_top_items_in_db

import requests
import os
import base64
import urllib.parse
import mysql.connector

import spotifyapi
from spotifyapi import SpotifyException
from collections import Counter


# Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)


BACKEND_DOMAIN = "127.0.0.1"
BACKEND_PORT = 5000
BACKEND_URL = f"http://{BACKEND_DOMAIN}:{BACKEND_PORT}"

FRONTEND_URL = "http://127.0.0.1:5173"

SPOTIFY_API_BASE_URL = "https://api.spotify.com"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = f"{BACKEND_URL}/redirect-spotify"
SCOPE = "user-read-private user-read-email user-top-read"


def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  
        database="music_project"
    )


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


@app.route("/redirect-spotify")
def redirect_spotify():
    """Handle Spotify's redirect"""
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

    # preparation de la connexion et les header pour interagir avec spotify
    db = get_db()
    cursor = db.cursor(dictionary=True)

    headers = {"Authorization": f"Bearer {access_token}"}


    # Récupérer les infos utilisateur et les stocker dans la DB
    me = spotifyapi.get_user_profile(access_token)
    email = me.get("email")
    username = me.get("display_name")
    picture_url = None
    if me.get("images") and len(me.get("images")) > 0:
        picture_url = me["images"][0]["url"]

    cursor.execute("SELECT ID_USERS FROM USERS WHERE EMAIL = %s", (email,))
    user = cursor.fetchone()

    # Ajout de l'utilisateur dans la DB s'il n'existe pas déjà
    if user:
        user_id = user["ID_USERS"]
    else:
        cursor.execute(
            "INSERT INTO USERS (USERNAME, EMAIL, PASSWORD_HASH, PICTURE_URL) VALUES (%s, %s, %s, %s)",
            (username, email, "spotify_oauth", picture_url)
        )
        db.commit()
        user_id = cursor.lastrowid

    # Met à jour les tops musiques et artistes de l'utilisateur dans la DB
    store_user_top_items_in_db(cursor, access_token, user_id)    

    db.commit()

    # Redirect to frontend with token
    resp = make_response(jsonify(token_info))
    resp.headers["Access-Control-Allow-Origin"] = "*"

    return redirect(f"{FRONTEND_URL}/redirect-spotify?token={access_token}")


@app.route("/profile")
def profile():
    # TODO : Récupérer les infos utilisateur depuis la DB au lieu de l'API Spotify
    print("[GET] /profile")
    token = request.args.get("token")

    if not token:
        resp = make_response(jsonify({"error": "No token provided"}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400

    headers = {"Authorization": f"Bearer {token}"}


    response = requests.get(f"{SPOTIFY_API_BASE_URL}/v1/me", headers=headers)

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
    # TODO : Récupérer les tops musiques depuis la DB au lieu de l'API Spotify
    print("[GET] /top-tracks")
    token = request.args.get("token")

    if not token:
        resp = make_response(jsonify({"error": "No token provided"}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400

    try:
        tracks = spotifyapi.get_top_tracks(token)
        # Récupérer les genres pour chaque morceau et les insérer dans top_genres
        for track in tracks:
            genres = get_track_genres(track, token)
            # TODO : Insérer les genres dans la DB si besoin
            track["genres"] = genres

        resp = make_response(jsonify(tracks))
        resp.headers["Access-Control-Allow-Origin"] = "*"

        return resp
    except SpotifyException as e:
        resp = make_response(
            jsonify({"error": str(e)})
        )
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, e.status_code



@app.route("/top-artists")
def top_artists():
    # TODO : Récupérer les tops artistes depuis la DB au lieu de l'API Spotify
    print("[GET] /top-artists")
    token = request.args.get("token")

    if not token:
        resp = make_response(jsonify({"error": "No token provided"}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400

    try:
        data = spotifyapi.get_top_artists(token)
        resp = make_response(jsonify(data))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp
    except SpotifyException as e:
        resp = make_response(
            jsonify({"error": str(e)})
        )
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, e.status_code



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
        f"{SPOTIFY_API_BASE_URL}/v1/tracks/{track_id}",
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

    data["compatibility_score"] = compute_track_compatibility(data)

    resp = make_response(jsonify(data))
    resp.headers["Access-Control-Allow-Origin"] = "*"

    return resp


@app.route("/track-research")
def track_research():
    print("[GET] /track-research")
    token = request.args.get("token")
    query = request.args.get("q")
    
    if not token:
        resp = make_response(jsonify({"error": "No token provided"}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400

    if not query:
        resp = make_response(jsonify({"error": "No query provided"}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400
    
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        f"{SPOTIFY_API_BASE_URL}/v1/search?q={urllib.parse.quote(query)}&type=track&limit=5",
        headers=headers,
    )

    print(f"Spotify API response status: {response.status_code}")

    if response.status_code != 200:
        resp = make_response(
            jsonify({"error": "Failed to fetch track research"})
        )
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, response.status_code

    data = response.json()

    tracks = data.get("tracks", {}).get("items", [])

    for track in tracks:
        track["compatibility_score"] = compute_track_compatibility(track)

    resp = make_response(jsonify(tracks))
    resp.headers["Access-Control-Allow-Origin"] = "*"

    return resp


def get_track_genres(track, token):
    """
    Récupère les genres associés à un morceau donné 
    (les genres associés à l'artiste principal) en utilisant l'API Spotify.
    """

    headers = {"Authorization": f"Bearer {token}"}
    artist_id = track["artists"][0]["id"]
    response = requests.get(
        f"{SPOTIFY_API_BASE_URL}/v1/artists/{artist_id}",
        headers=headers,
    )
    if response.status_code != 200:
        return []
    
    artist_data = response.json()
    return artist_data.get("genres", [])



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
    load_dotenv() # chargement des variables d'environnement depuis le fichier .env
    app.run(host=BACKEND_DOMAIN, port=BACKEND_PORT, debug=True) # lancement du serveur Flask