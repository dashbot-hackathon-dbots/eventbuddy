from microsoftbotframework import ReplyToActivity


def reply_dont_understand(message):
    ReplyToActivity(fill=message, text="Say what?!")
