from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Pokemon, poke_schema, pokemon_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/hiddenpage')
def hiddenpage():
    return { 'Apple bottom jeans': 'boots wit the furrr'}

@api.route('/pokedex', methods = ['POST'])
@token_required
def catch_pokemon(current_user_token):
    name = request.json['name']
    type = request.json['type']
    level = request.json['level']
    item = request.json['item']
    user_token = current_user_token.token

    print(f'Poke Test: {current_user_token.token}')

    pokeCaught = Pokemon(name, type, level, item, user_token=user_token)

    db.session.add(pokeCaught)
    db.session.commit()

    response = poke_schema.dump(pokeCaught)
    return jsonify(response)

#View Team
@api.route('/pokedex', methods = ['GET'])
@token_required
def openPokedex(current_user_token):
    a_user = current_user_token.token
    pokemons = Pokemon.query.filter_by(user_token = a_user).all()
    response = pokemon_schema.dump(pokemons)
    return jsonify(response)

#Update
@api.route('/pokedex/<id>', methods = ['POST', 'PUT'])
@token_required
def update_poke(current_user_token, id):
    pokeCaught = Pokemon.query.get(id)
    pokeCaught.name = request.json['name']
    pokeCaught.type = request.json['type']
    pokeCaught.level = request.json['level']
    pokeCaught.item = request.json['item']
    pokeCaught.user_toke = current_user_token.token

    db.session.commit()
    response = poke_schema.dump(pokeCaught)
    return jsonify(response)

#Delete
@api.route('/pokedex/<id>', methods = ['DELETE'])
@token_required
def delete(current_user_token, id):
    pokeCaught = Pokemon.query.get(id)
    db.session.delete(pokeCaught)
    db.session.commit()
    response = poke_schema.dump(pokeCaught)
    return jsonify(response)