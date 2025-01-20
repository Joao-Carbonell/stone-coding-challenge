from datetime import datetime
from marshmallow import ValidationError


def parse_date(date_str):
    """
    Parses a date string into a `datetime` object using predefined formats.

    This function attempts to parse the given date string into a `datetime` object.
    It iterates through a predefined list of date formats and uses `datetime.strptime`
    to convert the string. If the parsing is successful for a format, the corresponding
    `datetime` object is returned. If none of the formats match, a `ValueError` is raised.
    Next was chosen to iterate over the formats because it generates values on demand
    and do not store lists

    :param date_str: The date string that needs to be parsed.
    :type date_str: str
    :return: A `datetime` object corresponding to the parsed date string.
    :rtype: datetime.datetime
    :raises ValueError: When the provided date string does not match any of the predefined formats.
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
    try:
        return next(datetime.strptime(date_str.strip(), fmt) for fmt in formats if is_valid_format(date_str, fmt))
    except StopIteration:
        raise ValueError("DATE_INVALID_FORMAT")


def is_valid_format(date_str, fmt):
    """
    Validates whether a given date string matches a specified date format.

    This function checks if a given date string matches a specified date format

    :param date_str: The date string to be validated.
    :type date_str: str
    :param fmt: The date format string to validate against.
    :type fmt: str
    :return: A Boolean indicating whether the date string matches the given
        format. Returns True if the date string matches the format, and False
        otherwise.
    :rtype: bool
    """
    try:
        datetime.strptime(date_str.strip(), fmt)
        return True
    except ValueError:
        return False