# Documentation technique

Voir `README.md` pour les choix des technologies.

## Frontend

Tout le code lié au frontend est placé dans le dossier `frontend/`.

On retrouvera à la racine tous les fichiers de configuration, le dossier `node_modules/` contenant les dépendances javascript, le dossier `public/` contenant les ressources utiles au site, et enfin le dossier `src/` contenant le code source de l'application web.

### Organisation du dossier `frontend/src/`

Ce répertoire contient deux fichiers : `App.vue` contenant la logique faisant fonctionner le router, et `main.ts` qui crée l'application Vue et branche le router.

Il contient aussi plusieurs sous-répertoires :

- `assets/`

Ce répertoire contient principalement les fichiers de base css (très peu étant donné que l'on utilise Tailwind), et des images.

- `components/`

Ce répertoire contient tous les composants utilisés dans les vues. Dans le sous-répertoire `ui/` se trouve les composants de ShadcnUI.

- `composables/`

Tous les composables de l'application.

- `lib/`

Contient des constantes / des fonctions utiles pour l'application.

- `router/`

Contient la logique du router de l'application.

- `types/`

Ce répertoire contient des types Typescript utiles pour la gestion des données renvoyées par l'API.

- `views/`

Contient toutes les vues de l'application.


## Backend

Tout le code lié au backend est contenu dans le dossier `backend/`
Pour cela, nous avons utilisé le langage de programmation python en utilisant l'extension FLASK.
On retrouvera ainsi à la racine de ce dossier tous les fichiers contenant les codes permettant de récuperer et d'utiliser les données de spotify et de la db.

- `APICall.py` 

permet premièrement de connecter l'utilisateur en le redirigeant vers la page d'authentification utilisateur de Spotify et récupère les données d'écoute une fois connecté ce qui permet d'afficher le profil de 'utilisateur, les top musiques, les top artistes, le détail des musiques et aussi de faire des recherches de musiques via Spotify.

- `constants.py` 
 
permet de définir globalement les variables nécessaires utilisés dans différents scripts.

- `database.py` 
 
permet d'intéragir avec la base de données.

- `spotifyapi.py` 
 
permet d'intéragir avec la base de données

- `track_compatibility.py` 
 
permet de calculer la compatibilité entre les musiques.

## Bases de données

Le code lié à la bd est contenu dans le fichier db_projet-tutore.sql dans le dossier database/
Le backend s’appuie sur une base de données **MySQL** afin de stocker les informations des utilisateurs ainsi que leurs préférences musicales issues de l’API Spotify.

La connexion à la base de données est centralisée via la fonction `get_db()`, qui retourne un objet de connexion MySQL permettant d’exécuter les requêtes SQL depuis le backend Flask.

Les Tables sont :

USERS

Cette table stocke les informations de chaque utilisateur connecté via Spotify OAuth.

| Colonne     | Type         | Description                          |
| ----------- | ------------ | ------------------------------------ |
| ID          | INT (PK)     | Identifiant unique de l’utilisateur  |
| USERNAME    | VARCHAR(100) | Nom affiché de l’utilisateur Spotify |
| EMAIL       | VARCHAR(100) | Adresse email Spotify (unique)       |
| PICTURE_URL | VARCHAR(500) | URL de la photo de profil Spotify    |
| CREATED_AT  | TIMESTAMP    | Date de création de l’utilisateur    |


TOP_MUSICS

Cette table contient les musiques préférées de l’utilisateur, classées selon l’ordre renvoyé
| Colonne         | Type         | Description                          |
| --------------- | ------------ | ------------------------------------ |
| ID              | INT (PK)     | Identifiant interne                  |
| SPOTIFY_ID      | VARCHAR(100) | Identifiant Spotify de la musique    |
| USER_ID         | INT (FK)     | Référence à `USERS.ID`               |
| TRACK_NAME      | VARCHAR(255) | Nom de la musique                    |
| ARTIST_NAME     | VARCHAR(255) | Nom de l’artiste principal           |
| ALBUM_COVER_URL | VARCHAR(500) | Image de l’album                     |
| RANKING         | INT          | Rang dans le top Spotify             |
| DURATION_MS     | INT          | Durée du morceau en millisecondes    |
| POPULARITY      | INT          | Indice de popularité Spotify (0–100) |


TOP_ARTISTS

Cette table contient les artistes préférés de l’utilisateur.
| Colonne     | Type         | Description                                 |
| ----------- | ------------ | ------------------------------------------- |
| ID          | INT (PK)     | Identifiant interne                         |
| SPOTIFY_ID  | VARCHAR(100) | Identifiant Spotify de l’artiste            |
| USER_ID     | INT (FK)     | Référence à `USERS.ID`                      |
| ARTIST_NAME | VARCHAR(255) | Nom de l’artiste                            |
| PICTURE_URL | VARCHAR(255) | Image de l’artiste                          |
| FOLLOWERS   | INT          | Nombre d’abonnés Spotify                    |
| RANKING     | INT          | Rang dans le top artistes                   |
| SCORE       | INT          | Score interne utilisé pour la compatibilité |

TOP_GENRES

Cette table contient les genres musicaux dominants de l’utilisateur, déduits à partir des artistes et musiques écoutés.

| Colonne    | Type         | Description                                         |
| ---------- | ------------ | --------------------------------------------------- |
| ID         | INT (PK)     | Identifiant interne                                 |
| USER_ID    | INT (FK)     | Référence à `USERS.ID`                              |
| GENRE_NAME | VARCHAR(100) | Nom du genre musical                                |
| SCORE      | INT          | Poids du genre dans le profil utilisateur           |
| PERIOD     | VARCHAR(50)  | Période d’analyse (`short_term`, `long_term`, etc.) |



