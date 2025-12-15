from flask import Flask
from markupsafe import escape
from flask import request
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from random import randint


app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return 'Index Page'

def home():
    return "Hello, Flask !"


@app.route("/search")
def search():
    query = request.args.get('q', '')
    resp = make_response(jsonify({
        "results": [
            { "id": "music-1", "name": "Music 1", "artist": "Artist 1", "compatibility": randint(0, 100)/100 },
            { "id": "music-2", "name": "Music 2", "artist": "Artist 2", "compatibility": randint(0, 100)/100 },
            { "id": "music-3", "name": "Music 3", "artist": "Artist 3", "compatibility": randint(0, 100)/100 }
        ],
    }))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'
'''@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

@app.route("/me")
def me_api():
    user = get_current_user()
    return {
        "username": user.username,
        "theme": user.theme,
        "image": url_for("user_image", filename=user.image),
    }

@app.route("/users")
def users_api():
    users = get_all_users()
    return [user.to_json() for user in users]
'''
# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if valid_login(request.form['username'],
#                        request.form['password']):
#             return log_the_user_in(request.form['username'])
#         else:
#             error = 'Invalid username/password'
#     # the code below is executed if the request method
#     # was GET or the credentials were invalid
#     return render_template('login.html', error=error)

###### Appel d API ######


# app = Flask(__name__)

# @app.route("/call_api")
# def call_api():
#     response = request.get("https://api.github.com")
#     data = response.json()
#     return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
