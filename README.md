# Projet tutoré

Ben GAUDRY, Kevin BERTAUX, Daniel CAILLE, Wail BENSALEM

## Installation

### Frontend

```sh
cd frontend
npm install
```

### Backend

```sh
cd backend
pip install flask
pip install dotenv
pip install requests
pip install urllib
pip install mysql-connector-python
```

-> Demander le fichier `.env`

### Bases de données

Installer xampp avec MySQL.

Importer le fichier sql situé dans `database/` dans la base de données.


## Démarrage

Lancer le serveur XAMPP et MySQL.

Puis à la racine du projet :

- Windows :
```sh
.\start_all.bat
```

- Linux :
```
cd frontend
npm run dev

cd ../backend
python APICall.py
```


## Technologies

### Frontend

- NodeJS & npm
- Vite
- VueJS
- TypeScript
- ShadcnUI (librairie de composants)
- TailwindCSS

### Backend

- Python
- Flask

### Bases de données

- MySQL (MariaDB)
