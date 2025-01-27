from flask import request

from app.services.analytics_service import AnalyticsService


class AnalyticsController:
    """
    Provides methods related to analytics and productivity evaluation by specific periods
    with or without certain conditions. These methods act as controllers that handle
    request parsing and delegate the responsibility to the appropriate service layer.

    This controller is designed to process HTTP request arguments, map them to dictionaries
    and forward the processed data to the service layer methods in the form of a call, returning
    the service response back to the user.

    """
    @staticmethod
    def get_productivity_by_period():
        args = request.args.to_dict()
        return AnalyticsService.get_productivity_by_period(args)

    @staticmethod
    def get_productivity_by_period_with_angel():
        """
        Fetches productivity data for a specific time period along with associated
        aggregated data.

        This static method extracts arguments from the request object and
        delegates the processing to the `get_productivity_by_period_with_angel`
        method of the `AnalyticsService` class. It retrieves productivity metrics
        along with additional insights based on the provided parameters.

        :raises: Any exception encountered during argument extraction or in the
            service method call execution.
        :return: Aggregated productivity data for the specified period.
        :rtype: Any
        """
        args = request.args.to_dict()
        return AnalyticsService.get_productivity_by_period_with_angel(args)

    @staticmethod
    def get_productivity_by_angel():
        """
        Retrieves productivity data filtered by angel parameters.

        This static method extracts arguments from the HTTP request as a dictionary
        and passes them to the `get_productivity_by_angel` method of the
        `AnalyticsService` class for processing. The result is then returned.

        :raises TypeError: If the returned value from the service does not
            conform to the expected output type.

        :return: Productivity data retrieved based on specified parameters.
        :rtype: Any
        """
        args = request.args.to_dict()
        return AnalyticsService.get_productivity_by_angel(args)

    @staticmethod
    def get_productivity_by_logistics_pole_and_period():
        """
        Returns productivity analytics by logistics pole and period based on provided
        query parameters.

        This method extracts query parameters from the request object, converts them
        to a dictionary, and passes them to the corresponding service function to
        retrieve productivity data.

        :raises SomeException: Description of specific exception behavior if any.

        :rtype: dict
        :return: A dictionary containing productivity analytics data filtered by
            logistics pole and specified period.
        """
        args = request.args.to_dict()
        return AnalyticsService.get_productivity_by_logistics_pole_and_period(args)