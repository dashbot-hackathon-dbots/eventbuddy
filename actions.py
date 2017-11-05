from microsoftbotframework import ReplyToActivity


def reply_dont_understand(message):
    ReplyToActivity(fill=message, text="Say what?!").send()


# def reply_event_query(message):
