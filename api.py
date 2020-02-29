import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from models import db_drop_and_create_all, setup_db, Actor, Movie
from auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
!! NOTE uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES
@app.route("/actors", methods=["GET"])
@requires_auth("get:actors")
def get_actors(payload):
    '''
    get actors
    receive get request, return a list of actors
    '''
    actors = [a.format() for a in Actor.query.all()]
    # print(actors)
    return jsonify({"success": True, "actors": actors, "total": len(actors)})


@app.route("/actors", methods=["POST"])
@requires_auth("add:actor")
def create_actor(payload):
    '''
    create_actor

    receive post request, return the new actor id and a list of actors
    '''
    body = request.get_json()
    if not body:
        abort(422)

    new_name = body.get("name", None)
    new_age = body.get("age", None)
    new_gender = body.get("gender", None)

    if not new_name:
        abort(422)

    new_actor = Actor(name=new_name, age=new_age, gender=new_gender,)

    new_actor.insert()

    actors = [a.format() for a in Actor.query.all()]
    # print(actors)
    return jsonify({"success": True, "new_actor_id": new_actor.id, "actors": actors})


@app.route("/actors/<int:id>", methods=["DELETE"])
@requires_auth("delete:actor")
def delete_actor(payload, id):
    '''
    delete actor

    Receive delete request, then return deleted id and list of actors
    '''
    actor = Actor.query.filter(Actor.id == id).one_or_none()
    if not actor:
        abort(404)
    actor.delete()
    actors = [a.format() for a in Actor.query.all()]
    return jsonify({"success": True, "deleted_id": id, "actors": actors})


@app.route("/actors/<int:id>", methods=["PATCH"])
@requires_auth("modify:actor")
def update_actor(payload, id):
    '''
    update actor

    Receive patch request to update actor, then return list of actors
    '''
    # print(id)
    actor = Actor.query.filter(Actor.id == id).one_or_none()
    if not actor:
        abort(404)
    body = request.get_json()

    if not body:
        abort(422)
    new_name = body.get("name", None)
    new_age = body.get("age", None)
    new_gender = body.get("gender", None)

    if new_name is None:
        new_name = actor.name
    if new_age is None:
        new_age = actor.age
    if new_gender is None:
        new_gender = actor.gender

    actor.name = new_name
    actor.age = new_age
    actor.gender = new_gender

    actor.update()

    actors = [a.format() for a in Actor.query.all()]
    return jsonify({"success": True, "updated_id": id, "actors": actors})


"""
/movies
"""


@app.route("/movies", methods=["GET"])
@requires_auth("get:movies")
def get_movies(payload):
    '''
    get movies
    receive get request, return a list of movies
    '''
    movies = [m.format() for m in Movie.query.all()]
    return jsonify({"success": True, "movies": movies, "total": len(movies)})


@app.route("/movies", methods=["POST"])
@requires_auth("add:movie")
def create_movie(payload):
    '''
    create movie
    recieve post request, then return the new movie id, and list of movies
    '''
    body = request.get_json()
    if not body:
        abort(422)
    new_title = body.get("title", None)
    new_release = body.get("release", None)

    if not new_title:
        abort(422)

    new_movie = Movie(title=new_title, release=new_release)

    new_movie.insert()

    movies = [m.format() for m in Movie.query.all()]
    return jsonify({"success": True, "new_movie_id": new_movie.id, "movies": movies})


@app.route("/movies/<int:id>", methods=["DELETE"])
@requires_auth("delete:movie")
def delete_movie(payload, id):
    '''
    delete movie

    Receive delete request, then return deleted id and list of movies
    '''
    movie = Movie.query.filter(Movie.id == id).one_or_none()
    if not movie:
        abort(404)
    movie.delete()

    movies = [m.format() for m in Movie.query.all()]
    return jsonify({"success": True, "deleted_id": id, "movies": movies})


@app.route("/movies/<int:id>", methods=["PATCH"])
@requires_auth("modify:movie")
def update_moive(payload, id):
    '''
    update movie

    Receive patch request to update movies, then return list of movies
    '''
    movie = Movie.query.filter(Movie.id == id).one_or_none()
    if not movie:
        abort(404)
    body = request.get_json()

    if not body:
        abort(422)
    new_title = body.get("title", None)
    new_release = body.get("release", None)

    if new_title is None:
        new_title = movie.title
    if new_release is None:
        new_release = movie.release

    movie.title = new_title
    movie.release = new_release
    movie.update()

    movies = [m.format() for m in Movie.query.all()]
    return jsonify({"success": True, "updated_id": id, "movies": movies})


# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    '''
    error handling for unprocessable entity
    '''
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    '''
    error handler for 404
    '''
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource Not Found"
    }), 404


@app.errorhandler(400)
def bad_request(error):
    '''
    error for bad request
    '''
    return jsonify({
        "success": False,
        "error": 400,
        "Message": "Bad Request"
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    '''
    error for unallowed method
    '''
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not allowed"
    }), 405


@app.errorhandler(AuthError)
def not_auth(AuthError):
    '''
    error handler for AuthError
    '''
    return jsonify({
        "success": False,
        "error": AuthError.error['code'],
        "message": AuthError.error['description']
    }), 401
