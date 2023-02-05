from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix='/api')


# GET routes
@api.route('/cars')
@token_required
def get_cars(current_user_token):
    user = current_user_token.token
    cars = Car.query.filter_by(user_token = user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)


@api.route('/cars/<id>')
@token_required
def get_car(current_user_token, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)


# POST routes
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    color = request.json['color']
    accident_on_record = request.json['accident_on_record']
    user_token = current_user_token.token
    
    car = Car(make, model, year, color, user_token, accident_on_record)
    
    db.session.add(car)
    db.session.commit()
    
    response = car_schema.dump(car)
    return jsonify(response)


# PUT routes
@api.route('/cars/<id>', methods = ['PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.color = request.json['color']
    car.accident_on_record = request.json['accident_on_record']
    car.user_token = current_user_token.token
    
    db.session.commit()
    
    response = car_schema.dump(car)
    return jsonify(response)


# DELETE routes
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    
    db.session.delete(car)
    db.session.commit()
    
    response = car_schema.dump(car)
    return jsonify(response)