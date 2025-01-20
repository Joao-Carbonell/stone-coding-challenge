import unittest
from unittest.mock import patch
from flask import Flask
from app.controllers.attendance_controller import AttendanceController


class TestAttendanceCreation(unittest.TestCase):
    """
    Test suite for validating the functionalities of AttendanceController in creating and
    managing "attendance" records.

    The class is structured to test various scenarios for the `create_attendance` method,
    including valid and invalid input, ensuring proper validation, error handling, and
    interaction with the mocked database session.

    :ivar valid_data: A dictionary containing valid attendance data, used as the base
        reference for creating test cases with valid and invalid inputs.
    :type valid_data: dict
    """
    valid_data = {
        "id_attendance": 4,
        "id_client": 3,
        "angel": "JÃ´natas Neves Bandoli",
        "pole": "Rio de Janeiro",
        "deadline": "29/06/2021  09:09:30",
        "attendance_date": "28/06/2021  09:01:19"
    }

    def setUp(self):
        """
        Sets up the necessary test environment for Flask application testing. This
        includes initializing the Flask application, configuring it for testing
        purposes, and managing the application context. Additionally, the database
        session is mocked to prevent interactions with the actual database during tests.

        :raises unittest.mock.patched.StopAll: Ensures all active patchers are stopped
            after the test execution.

        :Attributes:
            app : Flask
                The Flask application initialized for testing.
            app_context : Flask.app_context
                The application context pushed to be available during tests.
            db_session_mock : unittest.mock.MagicMock
                A mock representation of the database session used to simulate
                database interaction during testing and prevent actual database
                modifications.
        :return: None
        """
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Mock the db session data
        self.db_session_mock = patch('app.config.config.db.session', autospec=True).start()
        self.addCleanup(patch.stopall)

    def tearDown(self):
        """
        Handles the teardown process for a testing environment by cleaning up resources
        allocated during a test case. Specifically, it ensures that the application
        context is properly removed and all temporary changes to the context stack
        are reverted.

        :raises RuntimeError: If no application context is active.
        """
        self.app_context.pop()

    def test_create_attendance_valid_data(self):
        """
        Test the creation of an attendance record with valid data.

        This unit test validates that the `create_attendance` method of the
        `AttendanceController` successfully creates an attendance record when
        provided with valid input data. The created object is verified to
        be persisted in the database, and the response returned is checked
        for the correct status code and message.

        :raises AssertionError: Raised if the response does not have the
            expected status code and message, or if the persistence calls
            to the mocked database session do not occur.

        :returns: None
        """

        response = AttendanceController.create_attendance(self.valid_data)

        # Check the response
        self.assertEqual(response.status_code, 201)
        self.assertIn('ATTENDANCE_CREATED', response.json['message'])

        # Check that object was persisted in db
        self.db_session_mock.execute.assert_called_once()
        self.db_session_mock.commit.assert_called_once()


    def test_create_attendance_empty_id_attendance(self):
        """
        Tests the behavior of the `create_attendance` method when provided with invalid
        input for the `id_attendance` field. Ensures that the service correctly identifies
        and reports the validation error without making any unintended changes to the
        underlying database.

        :raises AssertionError: If any of the test assertions do not hold true.
        """
        invalid_data = self.valid_data.copy()
        invalid_data["id_attendance"] = ""

        response = AttendanceController.create_attendance(invalid_data)

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

    def test_create_attendance_null_id_attendance(self):
        """
        Tests the behavior of the `create_attendance` method when the `id_attendance` field is
        missing in the input data. This test ensures that the service correctly identifies the
        missing required field, returns proper error responses, and does not proceed with
        database operations.

        :raises AssertionError: If the response status code is not 400, if the returned message
                                is incorrect, if 'errors' is not present in the response, if the
                                specific error messages related to `id_attendance` are missing,
                                or if any database operation is performed.
        """
        invalid_data = self.valid_data.copy()
        del invalid_data["id_attendance"]

        response = AttendanceController.create_attendance(invalid_data)

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

    def test_create_attendance_negative_id_attendance(self):
        """
        Test for the `create_attendance` method to ensure it does not allow creation
        of an attendance record when an invalid negative ID is provided. It validates
        that an error response is returned, and no database operations such as addition
        or commit are executed. This test enforces data integrity and checks for
        proper error handling in the service.

        :param invalid_data: Dictionary containing attendance data with an invalid
            negative ID.
        :type invalid_data: dict

        :return: The test does not return a value but instead uses assertions to
            validate the behavior of the method under test.
        """
        invalid_data = self.valid_data.copy()
        invalid_data["id_attendance"] = -1

        # Check the response
        response = AttendanceController.create_attendance(invalid_data)

        # Check the answer
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'INVALID_DATA')
        # self.assertEqual(response.json['error'], 'INVALID_ATTENDANCE_ID')

        self.assertIn('id_attendance', response.json['errors'])
        self.assertIn('INVALID_ATTENDANCE_ID', response.json['errors']['id_attendance'])

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()


    def test_create_attendance_empty_id_client(self):
        """
        Tests the creation of attendance with an empty `id_client` field to ensure
        proper validation is applied. This test verifies that the service rejects
        invalid data, returns the expected HTTP status code, error message, and does
        not interact with the database in case of validation failure.

        :param self: Reference to the current test case instance.
        :return: None
        """
        invalid_data = self.valid_data.copy()
        invalid_data["id_client"] = ""

        response = AttendanceController.create_attendance(invalid_data)

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

    def test_create_attendance_null_id_client(self):
        """
        Tests the creation of attendance with a null "id_client" field. This test ensures
        that the service correctly identifies and handles the invalid data where
        "id_client" is missing, returning proper error messages and status code.

        :raises AssertionError: If the response does not match the expected status code,
                                message, or validation errors; or if unintended database
                                operations are executed.
        """
        invalid_data = self.valid_data.copy()
        del invalid_data["id_client"]

        response = AttendanceController.create_attendance(invalid_data)

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

    def test_create_attendance_negative_id_client(self):
        """
        Tests the creation of an attendance record with an invalid client ID
        (negative value). The test checks the response from the service,
        the returned error messages, and verifies that no database operations
        are performed when the input data is invalid.

        :parameters:
            self : TestCase
                The instance of the test case class which provides context
                and setup for the test.

        :return: None
        """
        invalid_data = self.valid_data.copy()
        invalid_data["id_client"] = -1

        # Check the response
        response = AttendanceController.create_attendance(invalid_data)

        # Check the answer
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'INVALID_DATA')
        # self.assertEqual(response.json['error'], 'INVALID_ATTENDANCE_ID')

        self.assertIn('id_client', response.json['errors'])
        self.assertIn('INVALID_CLIENT_ID', response.json['errors']['id_client'])

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_create_attendance_empty_angel(self):
        """
        Tests the `create_attendance` method of `AttendanceController` for the scenario
        where an empty string is provided for the `angel` field. This test ensures
        that the service properly handles invalid data, does not perform any database
        operations, and returns the correct error message and status code.

        :param self: Reference to the current instance of the class.

        :return: None
        """
        invalid_data = self.valid_data.copy()
        invalid_data["angel"] = ""

        response = AttendanceController.create_attendance(invalid_data)

        # Check the answer
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'INVALID_DATA')
        # self.assertEqual(response.json['error'], 'INVALID_ATTENDANCE_ID')

        self.assertIn('angel', response.json['errors'])
        self.assertIn('INVALID_ANGEL_NAME', response.json['errors']['angel'])

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_create_attendance_null_angel(self):
        """
        Tests the creation of an attendance instance with missing 'angel' data, ensuring
        that invalid requests are handled appropriately. Verifies that the validation
        errors are captured and no database operations are executed.

        :raises AssertionError: If the test fails to meet expected conditions.
        """
        invalid_data = self.valid_data.copy()
        del invalid_data["angel"]

        response = AttendanceController.create_attendance(invalid_data)

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

    def test_create_attendance_not_string_angel(self):
        """
        Tests the behavior of the `create_attendance` function when the "angel" attribute in
        the input data is not a string. Ensures proper error handling and no unintended
        database operations are performed.

        :raises AssertionError: If any of the validations or test conditions fail.
        """
        invalid_data = self.valid_data.copy()
        invalid_data["angel"] = 6546546

        # Check the response
        response = AttendanceController.create_attendance(invalid_data)

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

    def test_create_attendance_empty_pole(self):
        """
        Test case to validate the behavior of the `AttendanceController.create_attendance` method when
        an empty string is provided for the 'pole' field in the input data. Ensures that the method
        handles invalid input appropriately and does not perform any operations on the database.

        :raises AssertionError: If the actual response does not match the expected status code,
            message, or error description.
        """
        invalid_data = self.valid_data.copy()
        invalid_data["pole"] = ""

        response = AttendanceController.create_attendance(invalid_data)

        # Check the answer
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'INVALID_DATA')
        # self.assertEqual(response.json['error'], 'INVALID_ATTENDANCE_ID')

        self.assertIn('pole', response.json['errors'])
        self.assertIn('INVALID_POLE_NAME', response.json['errors']['pole'])

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_create_attendance_null_pole(self):
        """
        Tests the scenario where attempting to create attendance with missing "pole"
        field results in appropriate validation errors and no changes to the database.

        Summary:
        This test case ensures that the `create_attendance` method in the
        AttendanceController behaves correctly when the required "pole" field is
        omitted from the data payload. The test validates both HTTP response and
        the absence of any database operations triggered due to invalid data.

        :param self: Test case instance for tracking the test context.
        :type self: TestCase
        """
        invalid_data = self.valid_data.copy()
        del invalid_data["pole"]

        response = AttendanceController.create_attendance(invalid_data)

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

    def test_create_attendance_not_string_pole(self):
        """
        Tests the behavior of the `AttendanceController.create_attendance` method when the input
        data contains an invalid non-string value for the "pole" field.

        The method is expected to validate the provided data, ensure that the field "pole" is a
        string, and return the appropriate error response upon invalid input.

        Attributes:
            invalid_data (dict): A copy of valid input data with a non-string value for the
            "pole" key.
            response (Response): The response returned from the method being tested.
            db_session_mock (Mock): A mocked instance of the database session to
            ensure no operations are executed on invalid input.

        Test Execution:
            1. Modify valid input data to include an invalid non-string value for the "pole"
               field.
            2. Call the `AttendanceController.create_attendance` method with the modified data.
            3. Verify that the response’s status code is 400.
            4. Validate the response’s JSON body includes the expected message and validation
               errors.
            5. Ensure no database operations (add or commit) are executed.

        Raises:
            AssertionError: If any of the test checks fail.

        """
        invalid_data = self.valid_data.copy()
        invalid_data["pole"] = 123123

        # Check the response
        response = AttendanceController.create_attendance(invalid_data)

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

    def test_create_attendance_invalid_attendance_date_type(self):
        """
        Tests the creation of an attendance entry with an invalid date format for the
        `attendance_date` field.

        This test ensures that the system identifies and rejects improperly formatted
        dates, returns the correct response status and error structure, and does not
        alter the database. It also verifies that no database operations are performed
        when invalid data is provided.

        :param self: Represents the instance of the test class.

        :raises AssertionError: If validations fail for expected response
            status, error structure, or database operation execution.

        :return: None
        """
        invalid_data = self.valid_data.copy()
        invalid_data["attendance_date"] = 123123


        response = AttendanceController.create_attendance(invalid_data)

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

    def test_create_attendance_invalid_formated_attendance_date(self):
        """
        Tests the creation of attendance with an invalidly formatted attendance date.

        This test ensures that the service properly handles invalid date formats
        by returning the expected response, error message, and status code. It also
        verifies that the database rollback method is triggered when the attendance
        creation fails due to a validation error.

        Raises assertion errors if the response does not meet expected conditions or
        if the database rollback is not called as expected.

        :param self: Instance of the current test class containing test case
            data and test setup.

        :return: None
        """
        invalid_data = self.valid_data.copy()
        invalid_data["attendance_date"] = "2023-05-01T14:00:00"

        response = AttendanceController.create_attendance(invalid_data)

        # Check the answer
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json['message'], 'ATTENDANCE_NOT_CREATED')
        self.assertEqual(response.json['error'], 'DATE_INVALID_FORMAT')

        # Check if the rollback was called
        self.db_session_mock.rollback.assert_called_once()

    def test_create_attendance_empty_attendance_date(self):
        """
        Tests the creation of attendance when the `attendance_date` is an empty string.
        This test ensures that the system properly handles and validates an invalid
        or empty attendance date and does not perform unnecessary database operations.

        :raises AssertionError: If the response or database operation behavior does not
            meet the expected outcomes.

        :param self: The instance of the test case.

        :return: None
        """
        invalid_data = self.valid_data.copy()
        invalid_data["attendance_date"] = ""

        response = AttendanceController.create_attendance(invalid_data)

        # Check the answer
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json['message'], 'ATTENDANCE_NOT_CREATED')
        self.assertEqual(response.json['error'], 'DATE_INVALID_FORMAT')

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_create_attendance_null_attendance_date(self):
        """
        Tests the behavior of the `create_attendance` function of the AttendanceController when the
        `attendance_date` is missing from the input data. This ensures proper validation of required
        fields, appropriate error messaging, and no unintended database modifications.

        :raises AssertionError: If the test assertions fail.
        """
        invalid_data = self.valid_data.copy()
        del invalid_data["attendance_date"]

        response = AttendanceController.create_attendance(invalid_data)

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

    def test_create_attendance_invalid_deadline_type(self):
        """
        Tests the creation of an attendance entity with an invalid deadline type.

        This test ensures that the application performs proper validation on the
        `deadline` field when an invalid type of data is provided. Specifically,
        this test checks if the system returns appropriate error messages and does
        not perform any database operations when invalid input data is supplied.

        :raises AssertionError: If the response code does not match the expected 400, if the error
            message details are missing or incorrect, or if the database operations
            are erroneously invoked during this scenario.
        """
        invalid_data = self.valid_data.copy()
        invalid_data["deadline"] = 1231231

        response = AttendanceController.create_attendance(invalid_data)

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

    def test_create_attendance_invalid_formated_deadline_date(self):
        """
        Tests the creation of an attendance record with an improperly formatted deadline date.

        Ensures that the system properly validates date format and returns an error response
        indicating that attendance creation has failed due to invalid date formatting. It also
        verifies that the database transaction was rolled back properly during the failure.

        :param invalid_data: The payload containing all required fields for attendance,
            but with the deadline field in an invalid format.
        :type invalid_data: dict

        :return: Asserts the failure response from the service including the corresponding error
            code and message, verifies that the rollback mechanism of the database is triggered.
        """
        invalid_data = self.valid_data.copy()
        invalid_data["deadline"] = "2023-05-01T14:00:00"

        response = AttendanceController.create_attendance(invalid_data)

        # Check the answer
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json['message'], 'ATTENDANCE_NOT_CREATED')
        self.assertEqual(response.json['error'], 'DATE_INVALID_FORMAT')

        # Check if the rollback was called
        self.db_session_mock.rollback.assert_called_once()

    def test_create_attendance_empty_deadline(self):
        """
        Tests the creation of attendance with an invalid empty deadline.

        This test ensures that when an attempt is made to create an attendance
        with an empty deadline, the system responds appropriately with a 500
        status code and accompanying error message. It also verifies that no
        changes are made to the database in this scenario.

        :raises AssertionError: If any of the following conditions are not met:
            - The response status code is 500.
            - The error message in the response JSON is 'ATTENDANCE_NOT_CREATED'.
            - The error field in the response JSON is 'DATE_INVALID_FORMAT'.
            - No database operations (add or commit) are executed.

        :return: None
        """
        invalid_data = self.valid_data.copy()
        invalid_data["deadline"] = ""

        response = AttendanceController.create_attendance(invalid_data)

        # Check the answer
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json['message'], 'ATTENDANCE_NOT_CREATED')
        self.assertEqual(response.json['error'], 'DATE_INVALID_FORMAT')

        # Check if no operation was executed in the db
        self.db_session_mock.execute.assert_not_called()
        self.db_session_mock.commit.assert_not_called()

    def test_create_attendance_null_deadline(self):
        """
        Tests the `create_attendance` method of `AttendanceController` to ensure it
        handles cases where the `deadline` field is missing in the provided
        data. This test verifies that proper validation is applied, correct error
        messages are returned, and no database operations are executed.

        #### Summary of Behavior:
        1. Removes the `deadline` field from provided data.
        2. Calls the `create_attendance` method with the modified data.
        3. Asserts that the returned HTTP status code is 400.
        4. Asserts that the correct error message 'INVALID_DATA' is returned.
        5. Confirms errors are present in the validation block for the missing
           `deadline` field.
        6. Asserts the database operations such as `add` and `commit` are not
           invoked due to invalid input.

        :param self: Reference to the test instance. Used to access test utilities
            and mocks.
        :return: None
        """
        invalid_data = self.valid_data.copy()
        del invalid_data["deadline"]

        response = AttendanceController.create_attendance(invalid_data)

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

    def test_create_attendance_unknown_field(self):
        """
        Test method for validating the behavior of the `create_attendance` method in `AttendanceController`
        when invalid data containing an unknown field is provided. Ensures that the service correctly
        handles unexpected or unrecognized fields by returning appropriate response codes and messages,
        and by not performing any database operations.

        :return: None
        """
        invalid_data = self.valid_data.copy()
        invalid_data["unknown_field"] = "unknown_field"

        response = AttendanceController.create_attendance(invalid_data)

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
