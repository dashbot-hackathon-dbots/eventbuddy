from datetime import datetime, timezone, timedelta

from microsoftbotframework import ReplyToActivity


def _make_dont_understand_reply(message):
    return ReplyToActivity(fill=message, text="Say what?!")


def reply_dont_understand(message, context):
    reply = _make_dont_understand_reply(message)
    return context, reply


def _date_to_datetime(date):
    return datetime(year=date.year, month=date.month, day=date.day)


def reply_event_query(message, context):
    question = context.get("question")
    message_text = message["text"]
    dont_understand_reply = _make_dont_understand_reply(message)
    if not context.get("suggestiongiven"):
        if question == "when":
            today = _date_to_datetime(datetime.now(tz=timezone.utc).date())
            tomorrow = today + timedelta(days=1)
            if message_text == "today":
                start = datetime.now(tz=timezone.utc).date()
                end = tomorrow
            elif message_text == "tomorrow":
                start = tomorrow
                end = start + timedelta(days=1)
            elif message_text == "next weekend":
                today = _date_to_datetime(datetime.now(tz=timezone.utc).date())
                start = _date_to_datetime(datetime.now(tz=timezone.utc).date()) + timedelta(days=12 - today.weekday() % 7)
                end = start + timedelta(days=2)
            else:
                return context, dont_understand_reply
            context["start"] = start
            context["end"] = end
        elif question == "where":
            if len(message_text) == 2:
                context["state_code"] = message_text
            else:
                return context, dont_understand_reply
        elif question == "genre":
            context["classification_names"] = message_text.split(",")
    start, end, state_code, classification_names = context.get("start"), context.get("end"),\
                                                   context.get("state_code"), context.get("classification_names")
    if start and end and state_code and classification_names:
        if context.get("suggestiongiven"):
            if message_text.lower() in ["yes", "great", "sounds good"]:
                context["proposepurchase"] = True
                reply = ReplyToActivity(fill=message,
                                        text="Great! Let's purchase the tickets then!")
            elif message_text.lower() in ["no", "nah", "meh"]:
                reply = ReplyToActivity(fill=message, text="Then what about...")
            else:
                return context, dont_understand_reply
        else:
            reply = ReplyToActivity(fill=message,
                                    text=str(context))  # TODO: Replace with suggestions
            context["suggestiongiven"] = True
    elif state_code and classification_names:
        reply = ReplyToActivity(fill=message,
                                text="When would you like to go? (options: today/tomorrow/next weekend))")
        context["question"] = "when"
    elif classification_names:
        reply = ReplyToActivity(fill=message, text="Where would you like to go?  (Supply state code. Example: CA)")
        context["question"] = "where"
    else:
        reply = ReplyToActivity(fill=message, text="What kind(s) of music do you like? (Separate by comma's)")
        context["question"] = "genre"
    return context, reply


def reply_ticket_purchase(message, context):
    print("b")
