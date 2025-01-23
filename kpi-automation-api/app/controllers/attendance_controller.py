from app.services.attendance_service import AttendanceService


class AttendanceController:
    """
    Handles attendance-related operations.

    Provides a static method for creating attendance records by
    delegating the responsibility to the AttendanceService. This
    class centralizes attendance management functions.

    """
    @staticmethod
    def create_attendance(data):
        """
        Creates an attendance record for the given input data by utilizing
        the AttendanceService.

        This method is responsible for interacting with the AttendanceService
        to create a new attendance record. It accepts the necessary input data
        and delegates the creation logic to the service.

        :param data: The input data required to create an attendance record.
        :type data: Any
        :return: The result of the attendance creation operation
                 as processed by the AttendanceService.
        :rtype: Any
        """
        return AttendanceService.create_attendance(data)

    @staticmethod
    def update_attendance(data, id):
        """
        Updates attendance records for a specific user.

        This method takes in attendance data and an identifier, validates the data using the
        `AttendanceSchema`, and updates attendance records by utilizing the
        `AttendanceService.update_attendance` function. If validation fails or other exceptions arise,
        appropriate error responses are returned.

        :param data: A dictionary containing attendance update data to be validated.
        :param id: An identifier for the user whose attendance is to be updated.
        :return: An HTTP response object. On success, returns the updated attendance data.
            On failure, returns an error message with a corresponding HTTP status code.
        """

        return AttendanceService.update_attendance(data, id)

    @staticmethod
    def retrieve_attendance(id):
        """
        Updates the attendance record by delegating to the AttendanceService.

        This function acts as a static method where it takes the attendance data
        and its corresponding unique identifier, passing these parameters to the
        `update_attendance` method in the `AttendanceService` class. The updated
        attendance information is then returned.

        :param id: Unique identifier for the attendance record to update.
        :type id: int
        :return: Updated attendance record data returned by AttendanceService.
        :rtype: dict
        """
        return AttendanceService.retrieve_attendance(id)

    @staticmethod
    def get_all_attendances(request):
        """
        Retrieve all attendance records based on the request arguments.

        This static method extracts the arguments from the provided request, converts
        them into a dictionary, and passes them to the attendance service to retrieve
        all attendance records.

        :param request: The incoming request object containing query parameters.
        :type request: flask.Request
        :return: A list of attendances retrieved based on the provided arguments.
        :rtype: List[dict]
        """
        args = request.args.to_dict()

        return AttendanceService.get_all_attendances(args)
