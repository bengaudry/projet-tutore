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

Tout le code liée au backend est contenu dans le dossier `backend/`
Pour cela, nous avons utilisé le langage de programmation python en utilisant l'extension FLASK.
On retrouvera ainsi à la racine de ce dossier tous les fichiers contenant le code permettant de communiquer avec l'API de spotify.

'APICall.py' permet premierement de connecter l'utilisateur en le redirigeant vers la page d'autentification utlisateur de spotify,
De plus, elle complete les données récuperé par celles déjà contenue dans la DB.
elle contient aussi les fonctions permettant d'afficher le profil de 'utilisateur, les top musiques, les top artistes, le détail des musiques et ainsi de permettre de faire des recherche de musiques via spotify.

'track_compatibility.py' permet de calculer la compatibilité d'une musique avec le profil de l'utilisateur actuel.

## Bases de données


Le backend utilise une base de données MySQL pour stocker les informations des utilisateurs et leurs préférences Spotify. La connexion à la base est gérée via la fonction get_db(), qui retourne un objet db permettant d’exécuter les requêtes SQL.

Tables principales

USERS

Cette table stocke les informations de chaque utilisateur connecté via Spotify OAuth.

| Colonne       | Type     | Description                                                |
| ------------- | -------- | ---------------------------------------------------------- |
| ID_USERS      | INT (PK) | Identifiant unique de l’utilisateur                        |
| USERNAME      | VARCHAR  | Nom affiché de l’utilisateur                               |
| EMAIL         | VARCHAR  | Email de l’utilisateur (unique)                            |
| PASSWORD_HASH | VARCHAR  | Mot de passe ou valeur spéciale "spotify_oauth" pour OAuth |
| CREATED_AT    | DATETIME | Date de création de l’utilisateur                          |

TOP_MUSICS

Cette table contient les musiques préférées de l’utilisateur, classées selon l’ordre renvoyé
| Colonne     | Type     | Description                                                  |
| ----------- | -------- | ------------------------------------------------------------ |
| USER_ID     | INT (FK) | Référence à `USERS.ID_USERS`                                 |
| TRACK_NAME  | VARCHAR  | Nom de la musique                                            |
| ARTIST_NAME | VARCHAR  | Nom de l’artiste                                             |
| RANKING     | INT      | Rang dans le top (1 = top 1)                                 |
| PERIOD      | VARCHAR  | Période d’analyse (`short_term`, `medium_term`, `long_term`) |

TOP_ARTISTS

Cette table contient les artistes préférés de l’utilisateur.
| Colonne     | Type     | Description                                                  |
| ----------- | -------- | ------------------------------------------------------------ |
| USER_ID     | INT (FK) | Référence à `USERS.ID_USERS`                                 |
| ARTIST_NAME | VARCHAR  | Nom de l’artiste                                             |
| RANKING     | INT      | Rang dans le top                                             |
| PERIOD      | VARCHAR  | Période d’analyse (`short_term`, `medium_term`, `long_term`) |



