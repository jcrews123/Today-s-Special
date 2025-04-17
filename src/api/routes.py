"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200



@api.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    all_users = [user.serialize() for user in users]
    
    return jsonify(all_users), 200


@api.route('/users', methods=['POST'])
def create_user():
    # Get the request body data
    body = request.get_json()
    
    # Check if email and password are provided
    if not body.get("email"):
        return jsonify({"error": "Email is required"}), 400
    
    if not body.get("password"):
        return jsonify({"error": "Password is required"}), 400
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=body["email"]).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400
    
    # Create new user
    new_user = User(
        email=body["email"],
        password=body["password"],  # In a real app, hash this password!
        is_active=body.get("is_active", True)
    )
    
    # Add and commit to database
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(new_user.serialize()), 201