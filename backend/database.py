"""
Fichier pour gérer les interactions avec la base de données
"""

import mysql.connector
import spotifyapi


def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  
        database="music_project"
    )


def get_user(email):
	"""Vérifie si un utilisateur existe dans la base de données."""

	db = get_db()
	cursor = db.cursor(dictionary=True)
	cursor.execute("SELECT id FROM Users WHERE email = %s", (email,))
	user = cursor.fetchone()
	cursor.close()
	return user


def register_user(username, email, picture_url):
	"""Enregistre un nouvel utilisateur dans la base de données."""

	db = get_db()
	cursor = db.cursor()
	cursor.execute(
		"INSERT INTO Users (username, email, picture_url) VALUES (%s, %s, %s)",
		(username, email, picture_url)
	)
	db.commit()
	return cursor.lastrowid


def clear_user_data(cursor, user_id):
	"""Supprime les données utilisateur existantes dans la base de données."""

	# Supprimer les données utilisateur existantes
	cursor.execute("DELETE FROM top_musics WHERE user_id = %s", (user_id,))
	cursor.execute("DELETE FROM top_artists WHERE user_id = %s", (user_id,))
	cursor.execute("DELETE FROM top_genres WHERE user_id = %s", (user_id,))


def store_genre(cursor, user_id, genre_name):
	"""Stocke un genre dans la base de données."""

	cursor.execute(
		"SELECT score FROM TOP_GENRES WHERE USER_ID = %s AND GENRE_NAME = %s",
		(user_id, genre_name)
	)

	genre_res = cursor.fetchone()
	genre_exists = genre_res is not None

	if genre_exists:
		cursor.execute(
			"""
			UPDATE TOP_GENRES
			SET score = %s
			WHERE USER_ID = %s AND GENRE_NAME = %s
			""",
			(genre_res[0] + 1, user_id, genre_name)
		)
	else:
		cursor.execute(
			"""
			INSERT INTO TOP_GENRES (USER_ID, GENRE_NAME, score)
			VALUES (%s, %s, %s)
			""",
			(user_id, genre_name, 1)
		)


def store_user_top_items_in_db(token, user_id):
	"""Récupère et stocke les tops musiques et artistes de l'utilisateur dans la base de données."""

	db = get_db()
	cursor = db.cursor()

	clear_user_data(cursor, user_id) # Nettoyer les données existantes avant d'insérer les nouvelles

    # Récupérer les tops artistes et les stocker dans la DB
	artists = spotifyapi.get_top_artists(token)

	for rank, artist in enumerate(artists, start=1):
		# Insère l'artiste dans la DB sinon
		cursor.execute(
			"""
			INSERT INTO TOP_ARTISTS (SPOTIFY_ID, USER_ID, ARTIST_NAME, PICTURE_URL, FOLLOWERS, RANKING, SCORE)
			VALUES (%s, %s, %s, %s, %s, %s, %s)
			""",
			(artist["id"],
			user_id,
			artist["name"],
			artist["images"][0]["url"] if artist.get("images") and len(artist.get("images")) > 0 else None,
			artist["followers"]["total"],
			rank,
			0)
		)

	# Récupérer les tops musiques et les stocker dans la DB
	tracks = spotifyapi.get_top_tracks(token)
	for rank, track in enumerate(tracks, start=1):
		# Met à jour le score de l'artiste si déjà présent dans les tops
		cursor.execute(
			"SELECT score FROM TOP_ARTISTS WHERE USER_ID = %s AND ARTIST_NAME = %s",
			(user_id, track["artists"][0]["name"])
		)
		prev_artist_score = cursor.fetchone()
		if prev_artist_score:
			new_artist_score = prev_artist_score[0] + 1
			cursor.execute(
				"""
				UPDATE TOP_ARTISTS
				SET score = %s
				WHERE USER_ID = %s AND ARTIST_NAME = %s
				""",
				(new_artist_score, user_id, track["artists"][0]["name"])
			)

		cursor.execute(
            """
            INSERT INTO TOP_MUSICS (SPOTIFY_ID, USER_ID, TRACK_NAME, ARTIST_NAME, ALBUM_COVER_URL, RANKING, DURATION_MS, POPULARITY)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (track["id"], user_id, track["name"],
			track["artists"][0]["name"],
			track["album"]["images"][0]["url"] if track.get("album") and track["album"].get("images") and len(track["album"]["images"]) > 0 else None,
			rank,
			track.get("duration_ms"),
			track.get("popularity"))
        )
		track_genres = spotifyapi.get_track_genres(track, token)
		for genre in track_genres:
			store_genre(cursor, user_id, genre)

	db.commit()
	cursor.close()


def get_user_profile(user_id):
	"""Récupère le profil de l'utilisateur depuis la base de données."""
	db = get_db()
	cursor = db.cursor(dictionary=True)
	cursor.execute("SELECT id, username, email, picture_url FROM users WHERE id = %s", (user_id,))
	data = cursor.fetchone()
	cursor.close()
	return data


def get_user_top_artists(user_id):
	"""Récupère les artistes les plus écoutés de l'utilisateur depuis la base de données."""
	db = get_db()
	cursor = db.cursor(dictionary=True)
	cursor.execute("SELECT id, spotify_id, artist_name AS name, picture_url, followers, score, ranking FROM top_artists WHERE user_id = %s ORDER BY ranking", (user_id,))	
	data = cursor.fetchall()
	cursor.close()
	return data


def get_user_top_tracks(user_id):
	"""Récupère les musiques les plus écoutées de l'utilisateur depuis la base de données."""
	db = get_db()
	cursor = db.cursor(dictionary=True)
	cursor.execute("SELECT id, spotify_id, track_name AS name, artist_name, album_cover_url, duration_ms, popularity FROM top_musics WHERE user_id = %s ORDER BY ranking", (user_id,))
	data = cursor.fetchall()
	cursor.close()
	return data


def get_user_top_genres(user_id):
	"""Récupère les genres les plus écoutés de l'utilisateur depuis la base de données."""
	db = get_db()
	cursor = db.cursor(dictionary=True)
	cursor.execute("SELECT id, genre_name, score FROM top_genres WHERE user_id = %s ORDER BY score DESC", (user_id,))
	data = cursor.fetchall()
	cursor.close()
	return data


def get_user_avg_popularity(user_id):
	"""Récupère la popularité moyenne des top musiques de l'utilisateur depuis la base de données."""
	db = get_db()
	cursor = db.cursor()
	cursor.execute("SELECT AVG(popularity) FROM top_musics WHERE user_id = %s", (user_id,))
	avg_popularity = cursor.fetchone()[0]
	cursor.close()
	return float(avg_popularity) if avg_popularity is not None else 0.0
