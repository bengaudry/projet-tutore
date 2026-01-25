from flask import Flask, redirect, session, make_response, jsonify, request
from dotenv import load_dotenv
from random import randint
from track_compatibility import compute_track_compatibility

import requests
import os
import base64
import urllib.parse
import mysql.connector
from collections import Counter


app = Flask(__name__)
app.secret_key = os.urandom(24)

BACKEND_DOMAIN = "127.0.0.1"
BACKEND_PORT = 5000
BACKEND_URL = f"http://{BACKEND_DOMAIN}:{BACKEND_PORT}"
FRONTEND_URL = "http://127.0.0.1:5173"

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

    # DONE : Récupérer les infos utilisateur et les stocker dans la DB
    me = requests.get("https://api.spotify.com/v1/me", headers=headers).json()
    email = me.get("email")
    username = me.get("display_name")

    cursor.execute("SELECT ID_USERS FROM USERS WHERE EMAIL = %s", (email,))
    user = cursor.fetchone()

    if user:
        user_id = user["ID_USERS"]
    else:
        cursor.execute(
            "INSERT INTO USERS (USERNAME, EMAIL, PASSWORD_HASH) VALUES (%s, %s, %s)",
            (username, email, "spotify_oauth")
        )
        db.commit()
        user_id = cursor.lastrowid

    # DONE : Récupérer les tops musiques, en déduire les tops genres et les stocker dans la DB
    tracks = requests.get(
        "https://api.spotify.com/v1/me/top/tracks?limit=50&time_range=short_term",
        headers=headers
    ).json().get("items", [])

    cursor.execute("DELETE FROM TOP_MUSICS WHERE USER_ID = %s", (user_id,))

    for rank, track in enumerate(tracks, start=1):
        cursor.execute(
            """
            INSERT INTO TOP_MUSICS (USER_ID, TRACK_NAME, ARTIST_NAME, RANKING, PERIOD)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, track["name"], track["artists"][0]["name"], rank, "long_term")
        )

    # DONE : Récupérer les tops artistes et les stocker dans la DB
    artists = requests.get(
        "https://api.spotify.com/v1/me/top/artists?limit=50&time_range=short_term",
        headers=headers
    ).json().get("items", [])

    cursor.execute("DELETE FROM TOP_ARTISTS WHERE USER_ID = %s", (user_id,))

    for rank, artist in enumerate(artists, start=1):
        cursor.execute(
            """
            INSERT INTO TOP_ARTISTS (USER_ID, ARTIST_NAME, RANKING, PERIOD)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, artist["name"], rank, "long_term")
        )

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
    # TODO : Récupérer les tops musiques depuis la DB au lieu de l'API Spotify
    print("[GET] /top-tracks")
    token = request.args.get("token")

    if not token:
        resp = make_response(jsonify({"error": "No token provided"}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400

    headers = {"Authorization": f"Bearer {token}"}


    response = requests.get(
        "https://api.spotify.com/v1/me/top/tracks?limit=50&time_range=short_term",
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
    tracks = data.get("items", [])

    # Récupérer l'utilisateur dans la DB via le token
    db = get_db()
    cursor = db.cursor(dictionary=True)

    response_me = requests.get("https://api.spotify.com/v1/me", headers=headers)
    if response_me.status_code != 200:
        resp = make_response(jsonify({"error": "Failed to fetch profile"}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, response_me.status_code

    email = response_me.json().get("email")
    cursor.execute("SELECT ID_USERS FROM USERS WHERE EMAIL = %s", (email,))
    user = cursor.fetchone()
    if not user:
        resp = make_response(jsonify({"error": "User not found"}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 404

    user_id = user["ID_USERS"]
    cursor.execute("DELETE FROM TOP_GENRES WHERE USER_ID = %s", (user_id,))

    # Récupérer les genres pour chaque morceau et les insérer dans TopGenres
    genre_counter = Counter()
    for track in tracks:
        genres = get_track_genres(track, token)
        # DONE : Insérer les genres dans la DB si besoin
        track["genres"] = genres
        for genre in genres:
            genre_counter[genre] += 1

    for rank, (genre, score) in enumerate(genre_counter.most_common(), start=1):
        cursor.execute(
            """
            INSERT INTO TOP_GENRES (USER_ID, GENRE_NAME, SCORE, RANKING, PERIOD)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, genre, score, rank, "short_term")
        )

    db.commit()

    resp = make_response(jsonify(tracks))
    resp.headers["Access-Control-Allow-Origin"] = "*"

    return resp


@app.route("/top-artists")
def top_artists():
    # TODO : Récupérer les tops artistes depuis la DB au lieu de l'API Spotify
    print("[GET] /top-artists")
    token = request.args.get("token")

    if not token:
        resp = make_response(jsonify({"error": "No token provided"}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        "https://api.spotify.com/v1/me/top/artists?limit=50&time_range=short_term",
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
        f"https://api.spotify.com/v1/search?q={urllib.parse.quote(query)}&type=track&limit=5",
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
        f"https://api.spotify.com/v1/artists/{artist_id}",
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