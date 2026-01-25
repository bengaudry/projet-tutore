import os
import base64
import requests
import urllib.parse

from flask import jsonify, make_response
from track_compatibility import compute_track_compatibility
from constants import BACKEND_URL


SPOTIFY_API_BASE_URL = "https://api.spotify.com"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = f"{BACKEND_URL}/redirect-spotify"
SCOPE = "user-read-private user-read-email user-top-read"


class SpotifyException(Exception):
    """Exception personnalisée pour les erreurs Spotify API."""

    def __init__(self, message, status_code=500):
        if message is None:
            message = "An unknown error occurred with the Spotify API."
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def get_authorization_url():
    """Construit l'URL de redirection vers la page d'autorisation de Spotify."""
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
    }
    return "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)



def get_access_token(code):
    """Échange le code d'autorisation contre un token d'accès."""
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

    access_token = token_info.get("access_token")

    if not access_token:
        raise SpotifyException(
            message=token_info.get('error_description', 'Failed to obtain access token from Spotify.'),
            status_code=response.status_code
        )

    return token_info


def get_user_profile(token):
    """Récupère le profil de l'utilisateur Spotify."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{SPOTIFY_API_BASE_URL}/v1/me", headers=headers)
    if response.status_code != 200:
        raise SpotifyException(
            message=response.json().get('error', {}).get('message', 'Unknown error'), 
            status_code=response.status_code
        )
    return response.json()


def get_top_artists(token):
    """Récupère les artistes les plus écoutés de l'utilisateur."""
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        f"{SPOTIFY_API_BASE_URL}/v1/me/top/artists?limit=50&time_range=short_term",
        headers=headers,
    )

    print(f"Spotify API response status: {response.status_code}")
    print(f"Spotify API response: {response.text}")

    if response.status_code != 200:
        raise SpotifyException(
            message=response.json().get('error', {}).get('message', 'Unknown error'), 
            status_code=response.status_code
        )

    data = response.json()
    return data.get("items", [])


def get_top_tracks(token):
    """Récupère les musiques les plus écoutées de l'utilisateur."""
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        f"{SPOTIFY_API_BASE_URL}/v1/me/top/tracks?limit=50&time_range=short_term",
        headers=headers,
    )

    print(f"Spotify API response status: {response.status_code}")

    if response.status_code != 200:
        raise SpotifyException(
            message=response.json().get('error', {}).get('message', 'Unknown error'),
            status_code=response.status_code
        )

    data = response.json()
    tracks = data.get("items", [])
    return tracks


def get_track_details(token, track_id):
    """Récupère les détails d'une musique spécifique."""

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{SPOTIFY_API_BASE_URL}/v1/tracks/{track_id}", headers=headers)

    if response.status_code != 200:
        raise SpotifyException(
            message=response.json().get('error', {}).get('message', 'Unknown error'),
            status_code=response.status_code
        )

    data = response.json()
    data["compatibility_score"] = compute_track_compatibility(data)
    return data


def get_track_research_results(token, query):
    """Recherche des musiques basées sur une requête."""

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{SPOTIFY_API_BASE_URL}/v1/search?q={query}&type=track&limit=5",
        headers=headers,
    )

    if response.status_code != 200:
        raise SpotifyException(
            message=response.json().get('error', {}).get('message', 'Unknown error'),
            status_code=response.status_code
        )

    data = response.json()

    tracks = data.get("tracks", {}).get("items", [])
    for track in tracks:
        track["compatibility_score"] = compute_track_compatibility(track)
        track["genres"] = get_track_genres(track, token)

    return tracks


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