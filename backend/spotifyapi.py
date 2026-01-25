import requests

SPOTIFY_API_BASE_URL = "https://api.spotify.com"

class SpotifyException(Exception):
    """Exception personnalisée pour les erreurs Spotify API."""

    def __init__(self, message, status_code=500):
        if message is None:
            message = "An unknown error occurred with the Spotify API."
        super().__init__(message)
        self.message = message
        self.status_code = status_code


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
