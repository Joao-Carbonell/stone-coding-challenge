import unittest
from unittest.mock import patch
from flask import Flask
from app.services.attendance_service import AttendanceService


class TestAttendanceUpdate(unittest.TestCase):
    """
    Unit tests for validating the `update_attendance` method in the AttendanceService class.

    This class contains unit tests for the `update_attendance` method of the AttendanceService,
    testing various scenarios involving both valid and invalid input data. It ensures that
    the method processes data correctly, handles errors appropriately, and interacts with the
    mocked database session as expected.

    :ivar valid_data: Contains a valid set of attendance data used for testing scenarios.
    :type valid_data: dict
    :ivar valid_id: A valid integer ID used for testing.
    :type valid_id: int
    """
    valid_data = {
        "id_attendance": 4,
        "id_client": 3,
        "angel": "JÃ´natas Neves Bandoli",
        "pole": "Rio de Janeiro",
        "deadline": "29/06/2021  09:09:30",
        "attendance_date": "28/06/2021  09:01:19"
    }
    valid_id = 1

    def setUp(self):

        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Mock the db session data
        self.db_session_mock = patch('app.config.config.db.session', autospec=True).start()
        self.addCleanup(patch.stopall)


    def tearDown(self):

        self.app_context.pop()

    def test_update_attendance_valid_data(self):
        """
        Tests the behavior of the `update_attendance` method when provided with valid data.

        This test case validates that the `update_attendance` method from the
        `AttendanceService` will successfully update attendance when valid inputs
        are passed. Additionally, it ensures that the method returns the correct
        status code and response message, and that the database operations are
        executed as expected.

        :raises AssertionError: If the response does not have a status code of 201, if
            the response message does not contain 'ATTENDANCE_UPDATED', or if the
            database operations are not called exactly once.
        """
        response = AttendanceService.update_attendance(self.valid_data,1)

        self.assertEqual(response.status_code, 201)
        self.assertIn('ATTENDANCE_UPDATED', response.json['message'])


        self.db_session_mock.execute.assert_called_once()
        self.db_session_mock.commit.assert_called_once()

    def test_update_attendance_invalid_id(self):
        """
        Tests the update_attendance method when provided with an invalid attendance ID.
        This test ensures that the service correctly handles the scenario of failing
        to update attendance records due to an invalid or empty identifier and that
        the proper error response is returned.

        :return: Nothing
        """
        response = AttendanceService.update_attendance(self.valid_data, "")


        self.assertEqual(response.status_code, 500)
        self.assertIn('ATTENDANCE_NOT_UPDATED', response.json['message'])

    def test_update_attendance_empty_id_attendance(self):
        """
        This test case verifies the behavior of the `update_attendance` method when
        provided with invalid data where the `id_attendance` field is an empty string.
        The test confirms that the method handles the invalid input with appropriate
        error messages, validation responses, and ensures no database operations occur.

        :raises AssertionError: If the response status code, json content, or validation
            behavior does not meet the expected outcomes.

        """
        invalid_data = self.valid_data.copy()
        invalid_data["id_attendance"] = ""

        response = AttendanceService.update_attendance(invalid_data, 1)

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'INVALID_DATA')

        # Check the specifics errors in the validation
        self.assertIn('errors', response.json)

        # Check the errors in "attendance_date"
        self.assertIn('id_attendance', response.json['errors'])
        self.assertIn('Not a valid integer.', response.json['errors']['id_attendance'])

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_update_attendance_null_id_attendance(self):
        """
        Tests the behavior of the `update_attendance` service when the required
        `id_attendance` field is missing from the provided data. Ensures the
        service correctly identifies the invalid data and does not perform any
        database operations.

        :raises AssertionError: If the response status code is not 400, if the error
                                message is not 'INVALID_DATA', or if the expected
                                validation errors are not present in the response.
        """
        invalid_data = self.valid_data.copy()
        del invalid_data["id_attendance"]

        response = AttendanceService.update_attendance(invalid_data, 1)

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'INVALID_DATA')

        # Check the specifics errors in the validation
        self.assertIn('errors', response.json)

        # Check the errors in "attendance_date"
        self.assertIn('id_attendance', response.json['errors'])
        self.assertIn('Missing data for required field.', response.json['errors']['id_attendance'])

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_update_attendance_negative_id_attendance(self):
        """
        Tests the `update_attendance` method of the AttendanceService when provided
        with invalid `id_attendance` data (specifically, a negative value).

        This test ensures that the service correctly identifies the invalid
        `id_attendance` value and returns an appropriate error response without
        executing any database operations.

        :raises AssertionError: If the returned status code, error message, or
            absence of database operations does not match the expected outcome.
        """
        invalid_data = self.valid_data.copy()
        invalid_data["id_attendance"] = -1

        # Check the response
        response = AttendanceService.update_attendance(invalid_data, 1)

        # Check the answer
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'INVALID_DATA')
        # self.assertEqual(response.json['error'], 'INVALID_ATTENDANCE_ID')

        self.assertIn('id_attendance', response.json['errors'])
        self.assertIn('INVALID_ATTENDANCE_ID', response.json['errors']['id_attendance'])

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_update_attendance_empty_id_client(self):
        """
        Tests the `update_attendance` method of the `AttendanceService` when the `id_client` field
        in the provided data is an empty string instead of a valid identifier. Verifies that the
        response indicates invalid data and checks the associated error messages.

        :return: None
        :raises AssertionError: If test assertions fail.
        """
        invalid_data = self.valid_data.copy()
        invalid_data["id_client"] = ""

        response = AttendanceService.update_attendance(invalid_data, 1)

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'INVALID_DATA')

        # Check the specifics errors in the validation
        self.assertIn('errors', response.json)

        # Check the errors in "id_client"
        self.assertIn('id_client', response.json['errors'])
        self.assertIn('Not a valid integer.', response.json['errors']['id_client'])

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_update_attendance_null_id_client(self):
        """
        Tests the `update_attendance` method of `AttendanceService` when the `id_client`
        field is missing in the provided data. Ensures the method handles the invalid
        data case correctly and does not execute any database operations.

        Attributes
        ----------
        valid_data : dict
            A dictionary with valid input data used as a template

        :return: None
        """
        invalid_data = self.valid_data.copy()
        del invalid_data["id_client"]

        response = AttendanceService.update_attendance(invalid_data, 1)

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'INVALID_DATA')

        # Check the specifics errors in the validation
        self.assertIn('errors', response.json)

        # Check the errors in "id_client"
        self.assertIn('id_client', response.json['errors'])
        self.assertIn('Missing data for required field.', response.json['errors']['id_client'])

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_update_attendance_negative_id_client(self):
        """
        Tests the behavior of the update_attendance method when the provided id_client is
        negative. Ensures that the service returns the appropriate error response and
        does not execute any database operations.

        :raises AssertionError: If the test fails due to an unexpected response or undesired
            database activity.


        :return: None. The function performs test assertions to validate the behavior of
            the tested method.
        """
        invalid_data = self.valid_data.copy()
        invalid_data["id_client"] = -1

        # Check the response
        response = AttendanceService.update_attendance(invalid_data, 1)

        # Check the answer
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'INVALID_DATA')
        # self.assertEqual(response.json['error'], 'INVALID_ATTENDANCE_ID')

        self.assertIn('id_client', response.json['errors'])
        self.assertIn('INVALID_CLIENT_ID', response.json['errors']['id_client'])

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_update_attendance_empty_angel(self):
        """
        Tests the behavior of the update_attendance function when an invalid data input
        is provided. Specifically, this test case validates the scenario in which the
        "angel" field is empty, and ensures proper error handling is triggered without
        unintended database operations.

        :raises AssertionError: If the response does not have the correct HTTP status
            code, error message, or does not contain appropriate error details.


        :return: Ensures that the response status code is 400, contains the correct
            error messages, and no database operations have been performed.
        """
        invalid_data = self.valid_data.copy()
        invalid_data["angel"] = ""

        response = AttendanceService.update_attendance(invalid_data, 1)

        # Check the answer
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'INVALID_DATA')
        # self.assertEqual(response.json['error'], 'INVALID_ATTENDANCE_ID')

        self.assertIn('angel', response.json['errors'])
        self.assertIn('INVALID_ANGEL_NAME', response.json['errors']['angel'])

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_update_attendance_null_angel(self):
        """
        Tests the scenario where the `angel` field is missing in the attendance update
        request. Ensures the system correctly identifies this missing field and returns
        an appropriate error response without performing any database operations.

        :raises AssertionError: If any of the expected conditions, such as response
            status, error message, or lack of database operations, are not met.
        """
        invalid_data = self.valid_data.copy()
        del invalid_data["angel"]

        response = AttendanceService.update_attendance(invalid_data, 1)

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'INVALID_DATA')

        # Check the specifics errors in the validation
        self.assertIn('errors', response.json)

        # Check the errors in "attendance_date"
        self.assertIn('angel', response.json['errors'])
        self.assertIn('Missing data for required field.', response.json['errors']['angel'])

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_update_attendance_not_string_angel(self):
        """
        Tests the update_attendance method of the AttendanceService for incorrect data
        type, specifically when the "angel" field is not provided as a string. The test
        verifies that the system behaves correctly by responding with a validation error
        and does not perform any database modifications.

        :raises AssertionError: If the status code or error messages do not match
            the expected values.
        :return: None
        """
        invalid_data = self.valid_data.copy()
        invalid_data["angel"] = 6546546

        # Check the response
        response = AttendanceService.update_attendance(invalid_data, 1)

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'INVALID_DATA')

        # Check the specifics errors in the validation
        self.assertIn('errors', response.json)

        # Check the errors in "attendance_date"
        self.assertIn('angel', response.json['errors'])
        self.assertIn('Not a valid string.', response.json['errors']['angel'])

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_update_attendance_empty_pole(self):
        """
        Tests the behavior of the `update_attendance` method when the `pole` field in the
        data payload is empty. Ensures that proper validation errors are returned and no
        database operations are executed.

        :raises AssertionError: If the HTTP response status code is not 400, if the
            error message is not 'INVALID_DATA', or if the expected errors in the `pole`
            field are not present in the response. Also raised if any database operations
            are performed.

        :return: None
        """
        invalid_data = self.valid_data.copy()
        invalid_data["pole"] = ""

        response = AttendanceService.update_attendance(invalid_data, 1)

        # Check the answer
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'INVALID_DATA')
        # self.assertEqual(response.json['error'], 'INVALID_ATTENDANCE_ID')

        self.assertIn('pole', response.json['errors'])
        self.assertIn('INVALID_POLE_NAME', response.json['errors']['pole'])

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_update_attendance_null_pole(self):
        """
        Test case for verifying the behavior of the AttendanceService when the 'pole'
        field is missing during update operation. This method ensures the service
        validates the input data correctly and returns the appropriate error response
        along with a proper validation message. It also guarantees that no database
        operations are executed in case of invalid data.

        :raises AssertionError: If any of the test assertions fail, indicating improper
            behavior of the AttendanceService or incorrect response validation.

        """
        invalid_data = self.valid_data.copy()
        del invalid_data["pole"]

        response = AttendanceService.update_attendance(invalid_data, 1)

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'INVALID_DATA')

        # Check the specifics errors in the validation
        self.assertIn('errors', response.json)

        # Check the errors in "attendance_date"
        self.assertIn('pole', response.json['errors'])
        self.assertIn('Missing data for required field.', response.json['errors']['pole'])

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_update_attendance_not_string_pole(self):
        """
        Tests for the `update_attendance` method of AttendanceService.

        The purpose of this test is to verify that the `update_attendance` method
        handles invalid input data properly when the "pole" field is not a string.
        It ensures that proper error handling and validation occur, including no
        unexpected database operations being executed.

        Test Details:
            - Modify the "pole" field to be an integer (`123123`) instead of a string.
            - Validate that the response has a status code of `400`.
            - Confirm that the error message in the response specifies `INVALID_DATA`.
            - Ensure that response contains validation errors under the "pole" field.
            - Check that no database operation is executed (e.g., no `execute` or
              `commit` methods are called).

        :raises AssertionError: If the response status code is not `400`, if the
                                error message is not `INVALID_DATA`, if specific
                                validation errors are not detected in the "pole" field,
                                or if database operations are unexpectedly performed.

        :return: None
        """
        invalid_data = self.valid_data.copy()
        invalid_data["pole"] = 123123

        # Check the response
        response = AttendanceService.update_attendance(invalid_data, 1)

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'INVALID_DATA')

        # Check the specifics errors in the validation
        self.assertIn('errors', response.json)

        # Check the errors in "attendance_date"
        self.assertIn('pole', response.json['errors'])
        self.assertIn('Not a valid string.', response.json['errors']['pole'])

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_update_attendance_invalid_attendance_date_type(self):
        """
        Tests the `update_attendance` method from `AttendanceService` to verify
        its behavior when the `attendance_date` field has an invalid data type.
        Ensures that the response contains appropriate error messages and no
        operation is performed on the database.

        :raises AssertionError: Raised if the evaluated conditions in assertions
            do not match the expected results.
        """
        invalid_data = self.valid_data.copy()
        invalid_data["attendance_date"] = 123123

        response = AttendanceService.update_attendance(invalid_data, 1)

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'INVALID_DATA')

        # Check the specifics errors in the validation
        self.assertIn('errors', response.json)

        # Check the errors in "attendance_date"
        self.assertIn('attendance_date', response.json['errors'])
        self.assertIn('DATE_INVALID_FORMAT', response.json['errors']['attendance_date'])

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_update_attendance_invalid_formated_attendance_date(self):
        """
        Tests the update_attendance method with an invalidly formatted attendance_date.

        This test case verifies that the AttendanceService properly validates the
        date format when updating attendance records. It ensures that an exception
        is raised and caught as intended, the appropriate error response is returned,
        and a rollback operation is performed in case of an invalid attendance_date
        format.

        Attributes:
            invalid_data (dict): A dictionary of input values for the update
                process, modified to include an invalid `attendance_date` string.
            response: The result returned by the `update_attendance` method call.
            db_session_mock: Mocked database session object used to verify
                rollback behavior.

        Raises:
            AssertionError: Raised when the test expectations fail, such as an
                incorrect HTTP response status, message, or rollback mechanism.

        :return: None
        """
        invalid_data = self.valid_data.copy()
        invalid_data["attendance_date"] = "2023-05-01T14:00:00"

        response = AttendanceService.update_attendance(invalid_data, 1)

        # Check the answer
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json['message'], 'ATTENDANCE_NOT_UPDATED')
        self.assertEqual(response.json['error'], 'DATE_INVALID_FORMAT')

        # Check if the rollback was called
        self.db_session_mock.rollback.assert_called_once()

    def test_update_attendance_empty_attendance_date(self):
        """
        Tests the behavior of the `update_attendance` method when an empty `attendance_date`
        is provided in the input data. It verifies that the system responds with an
        appropriate error message, status code, and ensures no database operation was
        performed due to invalid input.

        This test case ensures correctness of error handling and guards against
        inappropriate modifications to the database when invalid data is encountered.

        :raises AssertionError: If the returned status code, error message, or the
            method call behavior deviates from the expected output.
        """
        invalid_data = self.valid_data.copy()
        invalid_data["attendance_date"] = ""

        response = AttendanceService.update_attendance(invalid_data, 1)

        # Check the answer
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json['message'], 'ATTENDANCE_NOT_UPDATED')
        self.assertEqual(response.json['error'], 'DATE_INVALID_FORMAT')

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_update_attendance_null_attendance_date(self):
        """
        Tests the behavior of the AttendanceService when the attendance data does not contain
        the required `attendance_date` field. Ensures that proper validation errors are raised,
        and no database operations are performed if the data is invalid.

        :raises AssertionError: If the status code of the response is not 400, or if the
            validation error message is not present for the `attendance_date` field,
            or if any database operations are executed.
        :return: None
        """
        invalid_data = self.valid_data.copy()
        del invalid_data["attendance_date"]

        response = AttendanceService.update_attendance(invalid_data, 1)

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'INVALID_DATA')

        # Check the specifics errors in the validation
        self.assertIn('errors', response.json)

        # Check the errors in "attendance_date"
        self.assertIn('attendance_date', response.json['errors'])
        self.assertIn('Missing data for required field.', response.json['errors']['attendance_date'])

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_update_attendance_invalid_deadline_type(self):
        """
        Tests the behavior of ``AttendanceService.update_attendance`` when provided with an
        invalid type for the ``deadline`` field. Ensures that the method handles invalid
        data gracefully, does not perform any database operations, and returns the expected
        response with error messages.

        :raises AssertionError: If any of the assertions regarding response data, error
            messages, or database operations fail.
        """
        invalid_data = self.valid_data.copy()
        invalid_data["deadline"] = 1231231

        response = AttendanceService.update_attendance(invalid_data, 1)

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'INVALID_DATA')

        # Check the specifics errors in the validation
        self.assertIn('errors', response.json)

        # Check the errors in "attendance_date"
        self.assertIn('deadline', response.json['errors'])
        self.assertIn('DATE_INVALID_FORMAT', response.json['errors']['deadline'])

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_update_attendance_invalid_formated_deadline_date(self):
        """
        Tests updating attendance with an improperly formatted deadline date.

        This unit test verifies the behavior of the attendance update service
        when provided with a deadline date in an invalid format. Specifically,
        it ensures that the response contains the correct HTTP status code, error
        message, and error code. Additionally, it checks whether the rollback
        operation is invoked in case of the update failure.

        :raises AssertionError: If the observed response status code or
            error message does not match the expected values.
        :raises AssertionError: If the rollback operation is not called.

        """
        invalid_data = self.valid_data.copy()
        invalid_data["deadline"] = "2023-05-01T14:00:00"

        response = AttendanceService.update_attendance(invalid_data, 1)

        # Check the answer
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json['message'], 'ATTENDANCE_NOT_UPDATED')
        self.assertEqual(response.json['error'], 'DATE_INVALID_FORMAT')

        # Check if the rollback was called
        self.db_session_mock.rollback.assert_called_once()

    def test_update_attendance_empty_deadline(self):
        """
        Tests the behavior of the `update_attendance` method from the AttendanceService
        class when the provided data contains an empty string for the deadline field.
        This test ensures that the method correctly identifies the invalid input, does
        not perform any updates or database operations, and returns the expected error
        response.

        Attributes:
            valid_data (dict): A valid dictionary of attendance data used as the
                basis for invalid test input.

        :return: None
        """
        invalid_data = self.valid_data.copy()
        invalid_data["deadline"] = ""

        response = AttendanceService.update_attendance(invalid_data, 1)

        # Check the answer
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json['message'], 'ATTENDANCE_NOT_UPDATED')
        self.assertEqual(response.json['error'], 'DATE_INVALID_FORMAT')

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_update_attendance_null_deadline(self):
        """
        Tests the behavior of the `update_attendance` method in the `AttendanceService` when
        provided with invalid data missing the "deadline" field. This method verifies that
        the system rejects the operation and responds with proper error messages while
        ensuring no database operations are executed.


        :return: None.
        """
        invalid_data = self.valid_data.copy()
        del invalid_data["deadline"]

        response = AttendanceService.update_attendance(invalid_data, 1)

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'INVALID_DATA')

        # Check the specifics errors in the validation
        self.assertIn('errors', response.json)

        # Check the errors in "attendance_date"
        self.assertIn('deadline', response.json['errors'])
        self.assertIn('Missing data for required field.', response.json['errors']['deadline'])

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_update_attendance_unknown_field(self):
        """
        Tests the behavior of `update_attendance` when provided with invalid input data that
        contains an unknown field. This ensures that the function properly validates input data
        and prevents operations with unrecognized keys. Additionally, it verifies that no database
        operation occurs in case of validation failure.

        Attributes:
            invalid_data (dict): Copy of valid attendance data with a deliberately added unknown field.
            response (Response): The resulting response from the `update_attendance` method.

        Raises:
            AssertionError: If any of the asserted conditions do not hold.

        :return: None
        """
        invalid_data = self.valid_data.copy()
        invalid_data["unknown_field"] = "unknown_field"

        response = AttendanceService.update_attendance(invalid_data, 1)

        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'INVALID_DATA')

        # Check the specifics errors in the validation
        self.assertIn('errors', response.json)

        # Check the errors in "attendance_date"
        self.assertIn("unknown_field", response.json['errors'])
        self.assertIn("Unknown field.", response.json['errors']["unknown_field"])

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

if __name__ == '__main__':
    unittest.main()
