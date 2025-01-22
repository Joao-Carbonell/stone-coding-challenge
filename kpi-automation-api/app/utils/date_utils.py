from datetime import datetime, timedelta
from marshmallow import ValidationError


def parse_date(date_str):
    """
    Parses a date string into a datetime object based on one of several predefined formats.

    This function attempts to parse the input date string using multiple predefined formats.
    If the input string matches one of the formats, it returns a corresponding datetime object.
    If the string is invalid or does not match any of the formats, a ValueError is raised.

    :param date_str: The input date string to be parsed.
    :type date_str: str
    :return: A datetime object corresponding to the successfully parsed date string.
    :rtype: datetime
    :raises ValidationError: If `date_str` is not of type `str`.
    :raises ValueError: If `date_str` does not match any of the predefined formats, or if it is malformed.
    """
    #Validate the data type
    if not isinstance(date_str, str):
        raise ValidationError("DATE_INVALID_FORMAT")


    formats=[
        '%d/%m/%Y %H:%M:%S',  # 29/06/2021 10:15:27
        '%d/%m/%Y %H:%M',  # 29/06/2021 10:15
        '%d/%m/%Y',  # 30/06/2021
        '%d/%m%Y %H:%M',  # 30/062021 09:28
        '%Y-%m-%d %H:%M:%S',  # 2021-06-26 10:31:14
        '%d/%m/%y',  # 27/06/21
        '%d /%m /%Y %H:%M:%S'  # 28 /06 /2021 10:57:27
    ]
    # Return the date formated
    # If the formated date is invalid, return an exception
    # @TODO: Refactor to allow a empty field in the attendance_data field on db
    if date_str == '-':
        return datetime.now()
    try:
        return next(datetime.strptime(date_str.strip(), fmt) for fmt in formats if is_valid_format(date_str, fmt))
    except StopIteration:
        raise ValueError("DATE_INVALID_FORMAT "+str(date_str))


# Verify if the string is valid in date format
def is_valid_format(date_str, fmt):
    """
    Checks if the given date string matches the specified date format.

    This function takes a date string and a specified format, then validates
    if the string can be correctly parsed into a datetime object according to
    the given format. It returns a boolean value indicating whether the format
    is valid.

    :param date_str: The date string to validate.
    :type date_str: str
    :param fmt: The format to compare against for validation.
    :type fmt: str
    :return: True if the date string matches the format, False otherwise.
    :rtype: bool
    """
    try:
        datetime.strptime(date_str.strip(), fmt)
        return True
    except ValueError:
        return False

# Compare two dates to determine if the first one is greater than second.
# If so, return an exception, else return true
def compare_date(date1, date2):
    """
    Compares two dates and raises an error if the first date is after the
    second date. If the dates are in correct order, it returns True.

    :param date1: The start date to be compared.
    :type date1: datetime.date
    :param date2: The end date to be compared.
    :type date2: datetime.date
    :return: Boolean value indicating whether date1 is less than or equal
             to date2.
    :rtype: bool
    :raises ValueError: If date1 is greater than date2.
    """
    if date1 > date2:
        raise ValueError('END_DATE_GREATER_THAN_START_DATE')
    return True
# Count the number of days between two dates
# Used to determine the number of business days between two dates
def business_count_days(date1, date2):
    """
    Calculate the count of business days (Monday through Friday) between two dates,
    inclusive of the start and end dates.

    This utility function iterates over the date range starting from `date1`
    and ending at `date2` (both inclusive), and counts only the days that fall
    within Monday to Friday range. It excludes weekends (Saturday and Sunday)
    from the count.

    :param date1: The starting date of the range
    :type date1: datetime.date
    :param date2: The ending date of the range
    :type date2: datetime.date
    :return: The number of business days (excluding weekends) between `date1`
             and `date2`, inclusive
    :rtype: int
    """
    return sum(1 for day in (date1 + timedelta(days=i)
                                   for i in range((date2 - date1).days + 1))
                     if day.weekday() < 5)
