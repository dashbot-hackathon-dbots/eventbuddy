from datetime import datetime, timezone, timedelta
from random import choice

from microsoftbotframework import ReplyToActivity

from ticketmaster import find_events


def _make_dont_understand_reply(message):
    return ReplyToActivity(fill=message, text="Say what?!")


def reply_dont_understand(message, context):
    reply = _make_dont_understand_reply(message)
    return context, reply


def _date_to_datetime(date):
    return datetime(year=date.year, month=date.month, day=date.day)


def _get_event(context):
    events = find_events(
        start_date_time=context["start"], end_date_time=context["end"], state_code=context["state_code"],
        classification_names=context["classification_names"])
    music_events = [e for e in events for c in e.classifications if c.segment.name == "Music"]
    event = choice(music_events) if music_events else None
    if event:
        images = [i["url"] for i in event.json["images"]]
        image = images[0] if images else None
        venues = " / ".join([str(v) for v in event.venues])
        prices = " / ".join(["{} {} - {}".format(r["currency"], r["min"], r["max"]) for r in event.json.get("priceRanges", [])])
        classifications = " / ".join(["{} ({})".format(c.genre.name, c.subgenre.name) for c in event.classifications])
        event = {"name": event.name, "link": event.json["url"], "image": image,
                 "datetime": "{} {}".format(event.local_start_date, event.local_start_time),
                 "venues": venues, "classifications": classifications, "prices": prices}
    return event


def _build_event_message(event_dict, message, first=True):
    if first:
        prefix = "What do you think about?"
    else:
        prefix = "Then what about?"
    return ReplyToActivity(fill=message, text="{}\n\n{}\n{}\n{}\n{}{}".format(prefix,
        event_dict["name"], event_dict["classifications"], event_dict["datetime"],
        event_dict["prices"] + "\n" if event_dict.get("prices") else "",
        event_dict["venues"]), attachments=[{"contentType": "image/jpeg", "contentUrl": event_dict["image"]}])


def reply_event_query(message, context):
    question = context.get("question")
    message_text = message.get("text", "")
    dont_understand_reply = _make_dont_understand_reply(message)
    if not context.get("suggestiongiven"):
        if question == "when":
            today = _date_to_datetime(datetime.now(tz=timezone.utc).date())
            tomorrow = today + timedelta(days=1)
            if message_text == "today":
                start = _date_to_datetime(datetime.now(tz=timezone.utc).date())
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
        event = _get_event(context)
        if context.get("suggestiongiven"):
            if message_text.lower() in ["yes", "great", "sounds good", "nice"]:
                url = context["link"]
                context = {}
                context["proposepurchase"] = True
                reply = ReplyToActivity(fill=message, textFormat="markdown",
                                        text="Great! Let's [purchase]({}) the tickets then!".format(url))
            elif message_text.lower() in ["no", "nah", "meh", "next"]:
                if event:
                    reply = _build_event_message(event, message, first=False)
                    context["link"] = event["link"]
                else:
                    return {}, ReplyToActivity(fill=message, text="Sorry. I couldn't find anything to your taste!")
            else:
                return context, dont_understand_reply
        else:
            if event:
                reply = _build_event_message(event, message, first=True)
                context["link"] = event["link"]
            else:
                return {}, ReplyToActivity(fill=message, text="Sorry. I couldn't find anything to your taste!")
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
