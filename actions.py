from microsoftbotframework import ReplyToActivity


def reply_dont_understand(message, context):
    counter = context.get("counter", 0)
    ReplyToActivity(fill=message, text="Say what?! ({})".format(context.get("counter"))).send()
    return {"counter": counter+1}


# def reply_event_query(message, context):
#     user_id = message["from"]["id"]
#     context