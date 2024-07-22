from __future__ import annotations

import base64

from rest_framework.pagination import PageNumberPagination


def encode_text(text):
    """
    Encode a given text using Base64 encoding.

    Args:
        text (str): The text to encode.
    Returns:
        str: The Base64 encoded string.
    """
    text_bytes = text.encode('utf-8')
    encoded_bytes = base64.b64encode(text_bytes)
    encoded_text = encoded_bytes.decode('utf-8')
    return encoded_text


def decode_text(encoded_text):
    """
    Decode a given Base64 encoded text.

    Args:
        encoded_text (str): The Base64 encoded text to decode.
    Returns:
        str: The decoded string.
    """
    encoded_bytes = encoded_text.encode('utf-8')
    decoded_bytes = base64.b64decode(encoded_bytes)
    decoded_text = decoded_bytes.decode('utf-8')
    return decoded_text


class CustomPageNumberPagination(PageNumberPagination):
    """
    Handle Pagination
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
