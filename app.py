import os
import sys
from datetime import datetime

from flask import Flask, request, jsonify, abort
from flask_cors import CORS

from auth.auth import AuthError, requires_auth
from models.models import Actor, Movie, Appearance, setup_db


def create_app(config_file=os.path.join(os.getcwd(), 'config', 'dev_config.py')):
    # App Config
    app = Flask(__name__)

    database_path = os.environ.get('DATABASE_URL')
    if not database_path:
        app.config.from_pyfile(config_file)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path

    # Setup models
    setup_db(app)

    # CORS Headers
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE')
        return response

    @app.route('/')
    def hello():
        return 'Hello, World!'

    # ACTORS ENDPOINTS
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors-detail')
    def get_actors(payload):
        try:
            actors = [actor.describe() for actor in Actor.query.all()]
            return jsonify({
                "success": True,
                "actors": actors
            }), 200
        except BaseException:
            print(sys.exc_info())
            abort(404)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actor(payload):
        body = request.get_json()
        try:
            if any((element not in body for element in ('name', 'gender', 'birth_date'))):
                abort(422)

            new_actor = Actor(
                name=body['name'],
                gender=body['gender'],
                birth_date=datetime.strptime(body['birth_date'], '%Y-%m-%d'))
            new_actor.insert()

            return jsonify({
                'success': True,
                'new_actor': new_actor.describe()
            }), 200

        except BaseException:
            print(sys.exc_info())
            abort(404)

    @app.route('/actors/<id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actor_id(payload, id):
        body = request.get_json()
        try:
            patched_actor = Actor.query.get(id)

            for element in body:
                if element not in ('name', 'birth_date', 'gender'):
                    abort(422)
                setattr(patched_actor, element, body[element])

            patched_actor.update()

            return jsonify({
                "success": True,
                "patched_actor": patched_actor.describe()
            }), 200

        except BaseException:
            print(sys.exc_info())
            abort(404)

    @app.route('/actors/<id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor_id(payload, id):
        try:
            Actor.query.get(id).delete()
            return jsonify({
                "success": True,
                "delete": id
            }), 200
        except BaseException:
            print(sys.exc_info())
            abort(404)

    # MOVIES ENDPOINTS
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies-detail')
    def get_movies(payload):
        try:
            movies = [movie.describe() for movie in Movie.query.all()]
            return jsonify({
                "success": True,
                "movies": movies
            }), 200
        except BaseException:
            print(sys.exc_info())
            abort(404)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movie(payload):
        body = request.get_json()
        try:
            if any((element not in body for element in ('title', 'release_date'))):
                abort(422)

            new_movie = Movie(
                title=body['title'],
                release_date=datetime.strptime(body['release_date'], '%Y-%m-%d'))
            new_movie.insert()

            return jsonify({
                'success': True,
                'new_movie': new_movie.describe()
            }), 200

        except BaseException:
            print(sys.exc_info())
            abort(404)

    @app.route('/movies/<id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movie_id(payload, id):
        body = request.get_json()
        try:
            patched_movie = Movie.query.get(id)

            for element in body:
                if element not in ('title', 'release_date'):
                    abort(422)
                setattr(patched_movie, element, body[element])

            patched_movie.update()

            return jsonify({
                "success": True,
                "patched_movie": patched_movie.describe()
            }), 200

        except BaseException:
            print(sys.exc_info())
            abort(404)

    @app.route('/movies/<id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie_id(payload, id):
        try:
            Movie.query.get(id).delete()
            return jsonify({
                "success": True,
                "delete": id
            }), 200
        except BaseException:
            print(sys.exc_info())
            abort(404)

    # APPEARANCES ENDPOINTS
    @app.route('/appearances', methods=['POST'])
    @requires_auth('post:appearances')
    def post_appearance(payload):
        body = request.get_json()
        try:
            if any((element not in body for element in ('actor_id', 'movie_id'))):
                abort(422)

            new_appearance = Appearance(
                actor_id=body['actor_id'],
                movie_id=body['movie_id'],
            )
            new_appearance.insert()
            return jsonify({
                'success': True,
                'new_appearance': new_appearance.describe()
            }), 200

        except BaseException:
            print(sys.exc_info())
            abort(404)

    @app.route('/appearances', methods=['DELETE'])
    @requires_auth('delete:appearances')
    def delete_appearance(payload):
        body = request.get_json()
        try:
            if any((element not in body for element in ('actor_id', 'movie_id'))):
                abort(422)

            Appearance.query \
                .filter(Appearance.actor_id == body['actor_id'] and Appearance.movie_id == body['movie_id']) \
                .first() \
                .delete()

            return jsonify({
                "success": True,
                "delete": {'actor_id': body['actor_id'], 'movie_id': body['movie_id']}
            }), 200

        except BaseException:
            abort(404)

    # Error Handling
    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad Request'
        }), 400

    @app.errorhandler(401)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": 'Method Not Allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    return app


app = create_app()

if __name__ == '__main__':
    app.run()