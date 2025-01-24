from itertools import product

from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from app.controllers.analytics_controller import AnalyticsController
from app.controllers.attendance_controller import AttendanceController

productivity_blueprint = Blueprint('analytics', __name__, url_prefix="/api/analytics",
                                 description="Productivity analytics endpoints" )

# Routes for API's productivity endpoints
# @TODO: Add Schema for arguments and responses for all requests
@productivity_blueprint.route("/")
class ProductivityCollection(MethodView):

    @productivity_blueprint.response(200)
    @jwt_required()
    def get(self):
        """
        Handles GET request to the endpoint

        :return: A JSON response with a message
        """
        return {'message': 'Productivity API'}

@productivity_blueprint.route('/productivity_by_period/', methods=['GET'])
@jwt_required()
def get_productivity_by_period():
    """
    Handles the HTTP GET request to retrieve productivity analytics for a specific
    time period. This endpoint is designed to return insights on productivity metrics
    calculated over a given timeframe, as provided by the
    AnalyticsController's method.

    :returns: The productivity analytics information for the requested time period
        as provided by the AnalyticsController in an appropriate response format.
    :rtype: flask.Response
    """
    return AnalyticsController.get_productivity_by_period()

@productivity_blueprint.route('/productivity_by_period_with_angel/', methods=['GET'])
@jwt_required()
def get_productivity_by_period_with_angel():
    """
    Handles the HTTP GET request for retrieving productivity analytics by specified
    time periods with associated angel data.

    This endpoint fetches and returns productivity analytics in association with
    an "angel" entity. The specific functionality for data processing is delegated
    to the `AnalyticsController.get_productivity_by_period_with_angel()` method.

    :returns: The response from `AnalyticsController.get_productivity_by_period_with_angel()` method.
    """
    return AnalyticsController.get_productivity_by_period_with_angel()

@productivity_blueprint.route('/productivity_by_angel/', methods=['GET'])
@jwt_required()
def get_productivity_by_angel():

    return AnalyticsController.get_productivity_by_angel()

@productivity_blueprint.route('/productivity_by_logistics_pole_and_period/', methods=['GET'])
@jwt_required()
def get_productivity_by_logistics_pole_and_period():
    """
    Retrieves productivity data filtered by logistics pole and period.

    This function is part of the attendance blueprint and is responsible for
    fetching productivity-related analytics within specific logistical poles and
    periods, based on the requested parameters. It delegates the functionality
    to the AnalyticsController.

    :raises HTTPException: If the request fails or the query parameters are
        invalid.
    :return: Productivity data filtered by logistics pole and period.
    :rtype: Response
    """
    return AnalyticsController.get_productivity_by_logistics_pole_and_period()