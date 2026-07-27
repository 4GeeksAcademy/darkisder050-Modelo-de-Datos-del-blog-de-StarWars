"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/people', methods=['GET'])
def get_people():
    people = db.session.execute(db.select(People)).scalars().all()
    people_list = [ppl.serialize() for ppl in people]
    return jsonify(people_list), 200


@app.route("/people/<int:id>", methods=["GET"])
def get_people_id(id):
    person = db.get_or_404(People, id)
    return jsonify(person.serialize()), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = db.session.execute(db.select(Planet)).scalars().all()
    planets_list = [planet.serialize() for planet in planets]
    return jsonify(planets_list), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
    planet = db.get_or_404(Planet, planet_id)
    return jsonify(planet.serialize()), 200


@app.route('/users', methods=['GET'])
def get_users():
    users = db.session.execute(db.select(User)).scalars().all()
    users_list = [user.serialize() for user in users]
    return jsonify(users_list), 200


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():

    current_user_id = 1
    favorites = db.session.execute(
        db.select(Favorite).where(Favorite.user_id == current_user_id)
    ).scalars().all()

    favorites_list = [fav.serialize() for fav in favorites]
    return jsonify(favorites_list), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    current_user_id = 1

    db.get_or_404(Planet, planet_id)

    new_fav = Favorite(user_id=current_user_id, planet_id=planet_id)
    db.session.add(new_fav)
    db.session.commit()

    return jsonify({"msg": f"Planet {planet_id} added to favorites"}), 201


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    current_user_id = 1

    db.get_or_404(People, people_id)

    new_fav = Favorite(user_id=current_user_id, people_id=people_id)
    db.session.add(new_fav)
    db.session.commit()

    return jsonify({"msg": f"People {people_id} added to favorites"}), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    current_user_id = 1

    fav = db.session.execute(
        db.select(Favorite).where(
            Favorite.user_id == current_user_id,
            Favorite.planet_id == planet_id
        )
    ).scalar_one_or_none()

    if not fav:
        return jsonify({"error": "Favorite planet not found"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": f"Planet {planet_id} removed from favorites"}), 200


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    current_user_id = 1

    fav = db.session.scalars(
        db.select(Favorite).where(
        Favorite.user_id == current_user_id,
        Favorite.people_id == people_id
        )
    ).first()

    if not fav:
        return jsonify({"error": "Favorite people not found"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": f"People {people_id} removed from favorites"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
