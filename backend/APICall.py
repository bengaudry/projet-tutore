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
        email = me.get("email")
        username = me.get("display_name")
        picture_url = None
        if me.get("images") and len(me.get("images")) > 0:
            picture_url = me["images"][0]["url"]
        
        user_id = database.register_user(username, email, picture_url)

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

    try:
        tracks = database.get_user_top_tracks(user_id)
        resp = make_response(jsonify(tracks))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp
    except Exception as e:
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

    try:
        data = database.get_user_top_artists(user_id)
        resp = make_response(jsonify(data))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp
    except Exception as e:
        resp = make_response(
            jsonify({"error": str(e)})
        )
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 500


@app.route("/top-genres")
def top_genres():
    print("[GET] /top-genres")
    user_id = request.args.get("user_id")

    if not user_id:
        resp = make_response(jsonify({"error": "No user_id provided"}))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400

    try:
        data = database.get_user_top_genres(user_id)
        resp = make_response(jsonify([item['genre_name'] for item in data]))
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp
    except Exception as e:
        resp = make_response(
            jsonify({"error": str(e)})
        )
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 500


@app.route("/track-details")
def track_details():
    print("[GET] /track-details")
    token = request.args.get("token")
    user_id = request.args.get("user_id")
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
        data = spotifyapi.get_track_details(token, user_id, track_id)
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
    user_id = request.args.get("user_id")
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
        tracks = spotifyapi.get_track_research_results(token, user_id, query)
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
    