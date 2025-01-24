
from flask import make_response, jsonify
from jsonschema.exceptions import ValidationError

from app.repositories.attendance_repository import AttendanceRepository
from app.utils.date_utils import parse_date, compare_date, business_count_days


class AnalyticsService:

    @staticmethod
    def get_productivity_by_period(args):
        """
        Compute and retrieve productivity metrics for a specified date range.

        This method calculates the total attendances and productivity mean
        for multiple entities over a given range of business days. The
        result includes business days within the interval and calculated
        metrics for each entity.

        :param args: Dictionary containing 'start_date' and 'end_date',
            which define the date range for the productivity calculations.
        :type args: dict
        :return: A JSON response containing the calculated productivity
            details and business days, alongside a message indicating
            the retrieval status.
        :rtype: flask.Response
        :raises ValidationError: Raised if the 'start_date' or 'end_date'
            is missing in the input arguments.
        :raises ValueError: Raised if the provided date format is invalid.
        """
        try:
            if not args.get('end_date') or not args.get('start_date'):
                raise ValidationError("NO_DATE_SEND")

            start_date = parse_date(args.get('start_date'))
            end_date = parse_date(args.get('end_date'))

            compare_date(start_date, end_date)

            attendances = AttendanceRepository.get_attendances_by_period(start_date, end_date)

            business_days = business_count_days(start_date, end_date)

            result = list(map(lambda attendance: {
                'angel': attendance.angel,
                'total_attendances': attendance.total_attendances,
                'productivity_mean': attendance.total_attendances / business_days if business_days > 0 else 0
            }, attendances))

            business_days = {'business_days': business_days}

            result.append(business_days)

            return make_response(jsonify({'message':'PRODUCTIVITY_RETRIEVED', 'productivity_by_period': result}), 201)
        except ValueError as e:
            return jsonify({'message':'Invalid date format','error': str(e)}), 400
        except ValidationError as e:
            return jsonify({'message':'Need both start and end date.','error': str(e)}), 400

    @staticmethod
    def get_productivity_by_angel(args):
        try:
            if not args.get('angel'):
                raise ValidationError("NO_ANGEL_NAME_SEND")
    
            angel = args.get('angel')

            productivity_data = AttendanceRepository.get_productivity_by_angel(angel)

            if not productivity_data:
                return make_response(jsonify({'message': 'NO_DATA_FOUND'}), 404)

            business_days = business_count_days(productivity_data[0].start_date, productivity_data[0].end_date)

            result = list(map(lambda attendance: {
                'angel': attendance.angel,
                'total_attendances': attendance.total_attendances,
                'on_time_attendances': attendance.on_time_attendances,
                'delayed_attendances': attendance.total_attendances - attendance.on_time_attendances,
                'business_days': business_days,
                'productivity_mean': (attendance.total_attendances / business_days) if business_days > 0 else 0,
                'on_time_percentage': (attendance.on_time_attendances / attendance.total_attendances)
                                      * 100 if attendance.on_time_attendances  > 0 else 0
            }, productivity_data))

            return make_response(jsonify({'message':'PRODUCTIVITY_RETRIEVED', 'productivity_by_period': result}), 201)
        except ValueError as e:
            return jsonify({'message':'Invalid date format','error': str(e)}), 400
        except ValidationError as e:
            return jsonify({'message':'Missing data.','error': str(e)}), 400


    @staticmethod
    def get_productivity_by_period_with_angel(args):
        """
        Calculates the productivity report for a specified angel across a given date
        range. Retrieves productivity data for the specified angel by a requested
        date period, computes the overall productivity metrics, and returns the
        response as a JSON object.

        :param args: A dictionary containing the required keys:
            - 'start_date': The start date of the period (string in ISO format).
            - 'end_date': The end date of the period (string in ISO format).
            - 'angel': The name or identifier of the angel (string).
        :type args: dict

        :return: A JSON response encapsulating the message and calculated productivity
            metrics, or an error message when the input data is invalid. Productivity
            metrics include the angel name, total attendances, business days in the
            period, and the mean productivity.
        :rtype: Response
        """
        try:
            if not args.get('end_date') or not args.get('start_date'):
                raise ValidationError("NO_DATE_SEND")

            if not args.get('angel'):
                raise ValidationError("NO_ANGEL_NAME_SEND")

            start_date = parse_date(args.get('start_date'))
            end_date = parse_date(args.get('end_date'))

            compare_date(start_date, end_date)

            angel = args.get('angel')

            productivity_data = AttendanceRepository.get_productivity_by_period_with_angel(start_date, end_date, angel)

            if not productivity_data:
                return make_response(jsonify({'message': 'NO_DATA_FOUND'}), 404)

            business_days = business_count_days(start_date, end_date)

            result = list(map(lambda attendance: {
                'angel': attendance.angel,
                'total_attendances': attendance.total_attendances,
                'business_days': business_days,
                'productivity_mean': attendance.total_attendances / business_days if business_days > 0 else 0
            }, productivity_data))

            return make_response(jsonify({'message':'PRODUCTIVITY_RETRIEVED', 'productivity_by_period': result}), 201)
        except ValueError as e:
            return jsonify({'message':'Invalid date format','error': str(e)}), 400
        except ValidationError as e:
            return jsonify({'message':'Missing data.','error': str(e)}), 400

    @staticmethod
    def get_productivity_by_logistics_pole_and_period(args):
        """
        Calculate and retrieve productivity metrics for a specific logistics pole within a given period.

        This static method processes attendance data to calculate on-time and delayed attendance rates
        for a specified logistics pole between provided start and end dates. The calculation produces
        a set of percentage and total attendance metrics for further use.

        :param args: A dictionary containing the required parameters for processing attendance data.
            Should include the 'start_date' (str) and 'end_date' (str) representing the range of dates
            to analyze, and the 'pole' (str) representing the logistics pole name.

        :raises ValidationError: Raised if required arguments ('start_date', 'end_date', or 'pole')
            are missing or improperly supplied.
        :raises ValueError: Raised if the 'start_date' or 'end_date' values are not parseable as valid
            dates.

        :return: Returns a Flask JSON response containing a message and the calculated productivity data
            for the requested period and logistics pole. In case of errors, an appropriate error message
            and response status code are returned.
        :rtype: flask.Response
        """
        try:
            if not args.get('end_date') or not args.get('start_date'):
                raise ValidationError("NO_DATE_SEND")

            if not args.get('pole'):
                raise ValidationError("NO_POLE_NAME_SEND")

            start_date = parse_date(args.get('start_date'))
            end_date = parse_date(args.get('end_date'))

            compare_date(start_date, end_date)

            pole = args.get('pole')

            productivity_data = AttendanceRepository.get_productivity_by_logistics_pole_and_period(pole, start_date, end_date)

            if not productivity_data:
                return make_response(jsonify({'message': 'NO_DATA_FOUND'}), 404)

            result = list(map(lambda attendance: {
                'pole': attendance.pole,
                'total_attendances': attendance.total_attendances,
                'on_time_attendances': attendance.on_time_attendances,
                'delayed_attendances': attendance.total_attendances - attendance.on_time_attendances,
                'on_time_percentage': (attendance.on_time_attendances / attendance.total_attendances)
                                      * 100 if attendance.on_time_attendances  > 0 else 0
            }, productivity_data))

            return make_response(jsonify({'message': 'PRODUCTIVITY_RETRIEVED', 'productivity_by_period': result}), 201)
        except ValueError as e:
            return jsonify({'message': 'Invalid date format', 'error': str(e)}), 400

        except ValidationError as e:
            return jsonify({'message': 'Missing data.', 'error': str(e)}), 400

