from enum import Enum

class RequestAction(Enum):
    ACCEPT='accept'
    REJECT='reject'

RECEIVER_EMAIL_ID = 'receiver_email_id'
SENDER_EMAIL_ID = 'sender_email_id'