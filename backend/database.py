# Fichier pour gérer les interactions avec la base de données
import token
import mysql.connector

from backend.spotifyapi import get_top_artists, get_top_tracks

def clear_user_data(cursor, user_id):
	"""Supprime les données utilisateur existantes dans la base de données."""

	# Supprimer les données utilisateur existantes
	cursor.execute("DELETE FROM top_musics WHERE user_id = %s", (user_id,))
	cursor.execute("DELETE FROM top_artists WHERE user_id = %s", (user_id,))


def store_user_top_items_in_db(cursor, token, user_id):
	"""Récupère et stocke les tops musiques et artistes de l'utilisateur dans la base de données."""

	clear_user_data(cursor, user_id) # Nettoyer les données existantes avant d'insérer les nouvelles
	tracks = get_top_tracks(token)

	# Récupérer les tops musiques et les stocker dans la DB
	for rank, track in enumerate(tracks, start=1):
		cursor.execute(
            """
            INSERT INTO TOP_MUSICS (USER_ID, TRACK_NAME, ARTIST_NAME, RANKING, PERIOD)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, track["name"], track["artists"][0]["name"], rank, "long_term")
        )

    # Récupérer les tops artistes et les stocker dans la DB
	artists = get_top_artists(token)

	cursor.execute("DELETE FROM TOP_ARTISTS WHERE USER_ID = %s", (user_id,))

	for rank, artist in enumerate(artists, start=1):
		cursor.execute(
            """
            INSERT INTO TOP_ARTISTS (USER_ID, ARTIST_NAME, RANKING, PERIOD)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, artist["name"], rank, "long_term")
        )


def get_user_top_artists(cursor, user_id):
	pass


def get_user_top_tracks(cursor, user_id):
	"""Récupère les musiques les plus écoutées de l'utilisateur depuis la base de données."""
	cursor.execute("SELECT track_name, artist_name, album_cover_url FROM top_musics WHERE user_id = %s ORDER BY ranking", (user_id,))
	return cursor.fetchall()
