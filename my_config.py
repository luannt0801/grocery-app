"""Contains values and functions used in many modules."""

MY_ID = -1
CUSTOMER_ABSENT, CUSTOMER_LOGIN, CUSTOMER_EMAIL = (0, 1, 2)

APP_NAME = "Grocery App - Group 12"
ADMIN_PERM = 1

BACKGROUND = 'AntiqueWhite3'
FOREGROUND = 'AntiqueWhite1'
ERROR_FOREGROUND = 'red'


def is_float(value):
    """check whether it's float but also not throw error when it's string"""
    try:
        return isinstance(float(value), float)
    except ValueError:
        return False


def is_integer(value):
    """check whether it can be an int but also not throw error when it's string"""
    try:
        return isinstance(int(value), int)
    except ValueError:
        return False
