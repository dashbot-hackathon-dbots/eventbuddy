from actions import reply_dont_understand
from context import Contexts


class MessageHandler(object):

    contexts = Contexts()

    @staticmethod
    def determine_action(message_text, context):
        return reply_dont_understand

    @classmethod
    def handle_message(cls, message):
        if message["type"] == "message":
            user_id = message["from"]["id"]
            context = cls.contexts.get_context(user_id)
            action = cls.determine_action(message["text"], context)
            context = action(message, context)
            cls.contexts.set_context(user_id, context)
