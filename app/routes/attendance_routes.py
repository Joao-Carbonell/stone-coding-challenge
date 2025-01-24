from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from app.controllers.attendance_controller import AttendanceController

attendance_blueprint = Blueprint('attendances', __name__, url_prefix="/api/attendances",
                                 description="Attendance API endpoints" )

# Routes for Attendances API's endpoints
# @TODO: Add Schema for arguments and responses for all requests
@attendance_blueprint.route("/")
class AttendanceCollection(MethodView):
    """
    Handles attendance collection requests.

    This class represents a view for managing attendance collection. It is designed
    to handle various HTTP methods routed to the specified endpoint via Flask's
    MethodView, with primary emphasis on returning a JSON response using the GET
    request.

    :ivar decorators: A list of method decorators (Flask routing).
    :type decorators: list
    """

    @attendance_blueprint.response(200)
    @jwt_required()
    def get(self):
        """
        Handles GET request to the endpoint

        :return: A JSON response with a message
        """
        return {'message': 'Attendance API'}

@attendance_blueprint.route('/', methods=['POST'])
@jwt_required()
def create_attendance():
    """
    Handles the creation of a new attendance record. This function acts as the entry point
    for handling attendance creation requests within the application. It processes the
    incoming HTTP POST request containing attendance data in JSON format and delegates
    the handling to the `AttendanceController.create_attendance` method.

    :raises KeyError: Raised when required fields are missing in the request payload.
    :raises ValueError: Raised when provided data is invalid or its processing fails.
    :return: A response object containing the result of attendance creation, either a success message
             or an error response.
    :rtype: flask.Response
    :parameter
    """
    # Route for create an attendance
    return AttendanceController.create_attendance(request.json)

@attendance_blueprint.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_attendance(id):
    """
    Updates the attendance record specified by the given ID. This operation
    invokes the update functionality within the AttendanceController to
    update the attendance data based on the JSON payload received in the
    request.

    :param id: Unique identifier of the attendance record to be updated
    :type id: int
    :return: The response generated by the AttendanceController's
        update_attendance method, typically conveying the result of the
        update operation.
    """
    return AttendanceController.update_attendance(request.json, id)

@attendance_blueprint.route('/<int:id>', methods=['GET'])
@jwt_required()
def retrieve_attendance(id):
    """
    Handles the HTTP GET request to retrieve attendance details for a given
    attendance ID. This function routes requests via the AttendanceController
    to fetch the specified attendance record.

    :param id: The unique identifier of the attendance to retrieve
    :type id: int
    :return: A response object containing the attendance details or an error
        message if the record is not found
    :rtype: flask.Response
    """
    return AttendanceController.retrieve_attendance(id)

@attendance_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_attendances():
    """
    Retrieves a list of all attendances.

    This endpoint handles GET requests to fetch all attendance records. It
    communicates with the AttendanceController to retrieve the data and
    returns the result back to the requester.

    :returns: JSON representation of all attendance records.
    :rtype: flask.Response
    """
    return AttendanceController.get_all_attendances(request)


