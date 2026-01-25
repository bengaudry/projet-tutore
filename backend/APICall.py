from flask import Flask, redirect, make_response, jsonify, request
from dotenv import load_dotenv

import os

import database
import spotifyapi

from spotifyapi import SpotifyException
from constants import BACKEND_DOMAIN, BACKEND_PORT, FRONTEND_URL

# Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/begin-signin")
def beginSignin():
    """Redirect user to Spotify's authorization page"""
    print("[GET] /begin-signin")
    return redirect(spotifyapi.get_authorization_url())


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

    token_info = None

    try:
        token_info = spotifyapi.get_access_token(code)
    except SpotifyException as e:
        resp = make_response(
            jsonify({"error": f"Spotify API error: {e.message}"}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, e.status_code
    
    # Récupérer les infos utilisateur et les stocker dans la DB
    access_token = token_info.get("access_token")
    me = spotifyapi.get_user_profile(access_token)

    user = database.get_user(me.get("email"))

    # Ajout de l'utilisateur dans la DB s'il n'existe pas déjà
    if user:
        user_id = user["id"]
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


    # Met à jour les tops musiques et artistes de l'utilisateur dans la DB
    database.store_user_top_items_in_db(access_token, user_id)    

    # Redirect to frontend with token
    resp = make_response(jsonify(token_info))
    resp.headers["Access-Control-Allow-Origin"] = "*"

    return redirect(f"{FRONTEND_URL}/redirect-spotify?token={access_token}&userid={user_id}")


@app.route("/profile")
def profile():
    print("[GET] /profile")
    
    user_id = request.args.get("user_id")
    
    if not user_id:
        resp = make_response(jsonify({"error": "No user_id provided"}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400
    
    resp = make_response(jsonify(database.get_user_profile(user_id)))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp



@app.route("/top-tracks")
def top_tracks():
    print("[GET] /top-tracks")
    user_id = request.args.get("user_id")

    if not user_id:
        resp = make_response(jsonify({"error": "No user_id provided"}))
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
            jsonify({"error": str(e)})
        )
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 500



@app.route("/top-artists")
def top_artists():
    print("[GET] /top-artists")
    user_id = request.args.get("user_id")

    if not user_id:
        resp = make_response(jsonify({"error": "No user_id provided"}))
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
            jsonify({"error": str(e)})
        )
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 500



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
    
    try:
        data = spotifyapi.get_track_details(token, track_id)
        resp = make_response(jsonify(data))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp
    except SpotifyException as e:
        resp = make_response(
            jsonify({"error": f"Spotify API error: {e.message}"}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, e.status_code


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
    
    try:
        tracks = spotifyapi.get_track_research_results(token, query)
        resp = make_response(jsonify(tracks))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp
    except SpotifyException as e:
        resp = make_response(
            jsonify({"error": f"Spotify API error: {e.message}"})
        )
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, e.status_code


# Pour les tests :
@app.route("/")
def home():
    auth_url = (
        "https://accounts.spotify.com/authorize"
        f"?response_type=code&client_id={spotifyapi.CLIENT_ID}"
        f"&redirect_uri={spotifyapi.REDIRECT_URI}&scope={spotifyapi.SCOPE}"
    )
    return f"<a href='{auth_url}'>Se connecter avec Spotify</a>"



if __name__ == "__main__":
    load_dotenv() # chargement des variables d'environnement depuis le fichier .env
    app.run(host=BACKEND_DOMAIN, port=BACKEND_PORT, debug=True) # lancement du serveur Flask
    