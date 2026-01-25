import database
import spotifyapi


def compute_track_compatibility(token, user_id, track, top_tracks=None, top_artists=None, top_genres=None):
    """Calcule la compatibilité d'une musique avec le profil de l'utilisateur."""

    print("Calcul de la compatibilité pour la musique", track.get('name'), "de", track.get('artists')[0]['name'])

    if top_tracks is None:
        top_tracks = database.get_user_top_tracks(user_id)

    # Récupérer les artistes et genres préférés de l'utilisateur si non fournis
    if top_artists is None:
        top_artists = database.get_user_top_artists(user_id)
    if top_genres is None:
        top_genres = database.get_user_top_genres(user_id)

    track_artists = track.get('artists', [])
    track_genres = spotifyapi.get_track_genres(track, token)

    # Calcul des intersections entre genres et artistes de la musique et ceux des tops de l'utilisateur
    track_artists_in_top_artists = get_track_artists_in_top_artists(top_artists, track_artists)
    track_genres_in_top_genres = get_genres_in_top_genres(track_genres, top_genres)

    # Récupérer la popularité moyenne des musiques de l'utilisateur
    avg_popularity = database.get_user_avg_popularity(user_id)

    sum_of_genres_scores_in_top_genres = get_items_scores_sum(track_genres_in_top_genres)

    # Calcul des coefficients de compatibilité
    c1 = len(track_artists_in_top_artists) / max(len(track_artists), 1)    
    c2 = max(0,
        get_items_scores_sum(track_artists_in_top_artists) / max(get_items_scores_sum(top_artists), 1)
    )
    c3 = 1 - abs(track.get("popularity", 0)/100 - avg_popularity/100)

    if len(track_genres) == 0: # Pas de genres pour la musique, on ne prend pas en compte c4 et c5
        return (round(0.4*c1+0.4*c2+0.2*c3, 2), c1, c2, c3, 0, 0)

    c4 = len(track_genres_in_top_genres) / max(len(track_genres), 1)
    c5 = 0
    if sum_of_genres_scores_in_top_genres != 0:
        c5 = get_track_genres_score(track_genres, top_genres) / sum_of_genres_scores_in_top_genres

    return (round(0.3*c1+0.3*c2+0.1*c3+0.1*c4+0.2*c5, 2), c1, c2, c3, c4, c5)


def get_track_artists_in_top_artists(top_artists, track_artists):
    """Vérifie si les artistes d'une musique font partie des artistes préférés de l'utilisateur."""

    track_artists_names = {artist['name'] for artist in track_artists}

    matching_artists = []
    for artist in top_artists:
        if artist['name'] in track_artists_names:
            matching_artists.append(artist)

    return matching_artists


def get_items_scores_sum(items):
    sum = 0
    for item in items:
        sum += item['score']
    return sum


def get_track_genres_score(genres, top_genres):
    score = 0
    top_genres_names = {genre['genre_name']: genre['score'] for genre in top_genres}
    for genre in genres:
        if genre in top_genres_names:
            score += top_genres_names[genre]
    return score


def get_genres_in_top_genres(genres, top_genres):
    """Vérifie si les genres d'une musique font partie des genres préférés de l'utilisateur."""

    matching_genres = []
    for top_genre in top_genres:
        if top_genre['genre_name'] in genres:
            matching_genres.append(top_genre)
    
    return list(matching_genres)
