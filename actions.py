from microsoftbotframework import ReplyToActivity


def reply_dont_understand(message, context):
    counter = context.get("counter", 1)
    reply = ReplyToActivity(fill=message, text="Say what?! ({})".format(counter))
    return {"counter": counter+1}, reply


# def reply_event_query(message, context):
#     user_id = message["from"]["id"]
#     context