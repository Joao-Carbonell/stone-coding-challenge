from flask import Blueprint, request, jsonify, make_response
from app.models.attendance_model import User, db

attendance_blueprint = Blueprint('attendance', __name__)

@attendance_blueprint.route('/', methods=['GET'])
def home():
    return make_response(jsonify({'message': 'KPI API Gateway'}))


