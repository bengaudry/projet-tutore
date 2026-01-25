# Fichier pour gérer les interactions avec la base de données
import mysql.connector

def clear_user_data(cursor, user_id):
	"""Supprime les données utilisateur existantes dans la base de données."""

	# Supprimer les données utilisateur existantes
	cursor.execute("DELETE FROM top_musics WHERE user_id = %s", (user_id,))
	cursor.execute("DELETE FROM top_artists WHERE user_id = %s", (user_id,))
