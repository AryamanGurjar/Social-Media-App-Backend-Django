from __future__ import annotations

from social_media_app.constants import ERROR_MESSAGE_TEXT


class SocialMediaAppException(Exception):
    """
    Base class for exception.
    TODO: It can be extent further and more functionality can be added to this
    """

    def __init__(self, message=None):
        self.message = message or ERROR_MESSAGE_TEXT
        super().__init__(self.message)


class InvalidValue(SocialMediaAppException):
    """
    Raise exception if some value are not found or
    they are not provided in correct formate
    """

    message = 'Proper values are not provided!'
