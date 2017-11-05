import json

from actions import reply_dont_understand
from actions import reply_event_query
from actions import reply_ticket_purchase
from context import Contexts
import urllib3
import certifi
from fuzzywuzzy import fuzz

DASHBOT_API_KEY = "CLyJ1E8NKNzFbFZ45PUwXmLAGkZCZiajlsBuXHDU"

http = urllib3.PoolManager(block=True, cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

sub_classifications = ["hiphop", "jazz", "rock"]
interested_in_event = ["yes", "yeah", "yap", "interested"]

MATCHING_TOLERANCE = 50

class MessageHandler(object):

    contexts = Contexts()

    @staticmethod
    def update_max_score(max_match, message, strings_list, cur_cls):
        for string in strings_list:
            score = fuzz.ratio(message, string)
            if score > max_match["score"]:
                max_match["score"] = score
                max_match["class"] = cur_cls

    @classmethod
    def determine_action(cls, message_text, context):
        max_match = {"score": 0, "class": reply_dont_understand}
        cls.update_max_score(max_match, message_text, sub_classifications, reply_event_query)
        cls.update_max_score(max_match, message_text, interested_in_event, reply_ticket_purchase)
        if max_match["score"] < MATCHING_TOLERANCE:
            return reply_dont_understand
        return max_match["class"]

    @staticmethod
    def call_dashbot(direction, user_id, message_text):
        url = "https://tracker.dashbot.io/track?platform=generic&v=9.3.0-rest&type={}&apiKey={}".format(
            direction, DASHBOT_API_KEY)
        data = json.dumps({"text": message_text, "userId": user_id})
        r = http.request("POST", url, body=data, headers={'Content-Type': 'application/json'})

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
