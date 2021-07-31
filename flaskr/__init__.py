from flask import Flask, request, jsonify, abort
from .database.models import setup_db, Actor, Movie, create_and_drop_all
from flask_cors import CORS
import sys
import datetime
from werkzeug.exceptions import HTTPException, NotFound, PreconditionFailed

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    # cors headers allow
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             "Content-Tpe,Authorization,true")
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,PATCH,DELETE,OPTIONS')
        return response

    # routes
    ''' sample route '''
    @app.route('/')
    def index():
        return jsonify({
            "success": True,
            "message": "Hello, World!"
        })

    # routes for movies
    @app.route('/movies')
    # @requires_auth('view:movies')
    def get_movies():
        print("\n\nGet movies api hit:\n\n")
        try:
            movies = Movie.query.all()
            if movies is None:
                abort(404)
            movies = [movie.get_formatted_json() for movie in movies]
            return jsonify(movies)
        except:
            print(sys.exc_info())
            abort(422)

    @app.route('/movies', methods=['POST'])
    def create_movie():
        print("Post api on /movies hit:\n\n")
        try:
            data = request.get_json()
            print(data, '\n\n')
            movie = Movie(title=data['title'],
                          release_date=datetime.date.fromisoformat(data['release_date']), genre=data['genre'])
            movie.insert()
            print(movie, "created\n\n")
            return jsonify({
                "success": True,
                "movie_id": movie.id
            })
        except:
            print(sys.exc_info())
            abort(422)

    @app.route('/movie/<int:movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        print("Delete api on /movie hit:\n\n")
        try:
            print(movie_id, '\n\n')
            movie = Movie.query.get(movie_id)
            if movie is None:
                abort(404)
            movie.delete()
            print(movie, "deleted\n\n")
            return jsonify({
                "success": True,
                "deleted": movie.id
            })
        except NotFound as e:
            print(sys.exc_info())
            abort(404)
        except:
            print(sys.exc_info())
            abort(422)

    # routes for actors
    @app.route('/actors')
    # @requires_auth('view:actors')
    def get_actors():
        print("\n\nGet actors api hit:\n\n")
        try:
            actors = Actor.query.all()
            if actors is None:
                abort(404)
            actors = [actor.get_formatted_json() for actor in actors]
            return jsonify({
                "success": True,
                "actors": actors
            })
        except:
            print(sys.exc_info())
            abort(422)

    @app.route('/actors', methods=['POST'])
    def create_actor():
        print("Post api on /actors hit:\n\n")
        try:
            data = request.get_json()
            print(data, '\n\n')
            actor = Actor(name=data['name'],
                          age=data['age'], gender=data['gender'])
            actor.insert()
            print(actor, "created\n\n")
            return jsonify({
                "success": True,
                "actor_id": actor.id
            })
        except:
            print(sys.exc_info())
            abort(422)

    @app.route('/actor/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        print("Delete api on /actor hit:\n\n")
        try:
            print(actor_id, '\n\n')
            actor = Actor.query.get(actor_id)
            if actor is None:
                abort(404)
            # actor.delete()
            print(actor, "deleted\n\n")
            return jsonify({
                "success": True,
                "deleted": actor.id
            })
        except NotFound as e:
            print(sys.exc_info())
            abort(404)
        except:
            print(sys.exc_info())
            abort(422)

        # error handlers :

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(412)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 412,
            "message": "Precondition for resouce failed",
            "question": False
        }), 412

    @app.errorhandler(404)
    def error_resource_not_found(error):
        return jsonify({
            "success": False,
            "message": "Resource not found",
            "error": 404
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "message": "Internal server error",
            "error": 500
        }), 500

    @app.errorhandler(422)
    def not_processable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Request cant be processed"
        }), 422

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(401)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Not Authorized"
        })

    @app.errorhandler(403)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden"
        }), 403

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
