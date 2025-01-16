from flask import Blueprint, jsonify, make_response

general_blueprint = Blueprint('general', __name__)


@general_blueprint.route('/', methods=['GET'])
def home():
    return make_response(jsonify({'message': 'Pedra Pagamentos'}))
