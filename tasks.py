import json

from actions import reply_dont_understand
from context import Contexts
import urllib3
import certifi

DASHBOT_API_KEY = "CLyJ1E8NKNzFbFZ45PUwXmLAGkZCZiajlsBuXHDU"

http = urllib3.PoolManager(block=True, cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())


class MessageHandler(object):

    contexts = Contexts()

    @staticmethod
    def determine_action(message_text, context):
        return reply_dont_understand

    @staticmethod
    def call_dashbot(direction, user_id, message_text):
        url = "https://tracker.dashbot.io/track?platform=generic&v=9.3.0-rest&type={}&apiKey={}".format(
            direction, DASHBOT_API_KEY)
        data = json.dumps({"text": message_text, "userId": user_id})
        r = http.request("POST", url, body=data, headers={'Content-Type': 'application/json'})
        print(r)

    @classmethod
    def handle_message(cls, message):
        if message["type"] == "message":
            user_id = message["from"]["id"]
            context = cls.contexts.get_context(user_id)
            in_message_text = message["text"]
            cls.call_dashbot("incoming", user_id, in_message_text)
            action = cls.determine_action(in_message_text, context)
            context, reply = action(message, context)
            out_message_text = reply.text
            reply.send()
            cls.call_dashbot("outgoing", user_id, out_message_text)
            cls.contexts.set_context(user_id, context)
