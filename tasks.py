from microsoftbotframework import ReplyToActivity
from actions import reply_dont_understand


def determine_action(message_text):
    return reply_dont_understand


def handle_message(message):
    if message["type"] == "message":
        action = determine_action(message["text"])
        action(message)