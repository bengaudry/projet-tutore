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



## Bases de données


