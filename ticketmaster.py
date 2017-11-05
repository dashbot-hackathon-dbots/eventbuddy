import ticketpy


def find_events(start_date_time, end_date_time, classification_names, state_code):
    tm_client = ticketpy.ApiClient('4KEuLm3GnFY5e8ROVqrn8aUvwUYGO4AL')
    pages = tm_client.events.find(
        classification_name=classification_names,
        state_code=state_code,
        start_date_time=start_date_time.isoformat(timespec='seconds') + "Z",
        end_date_time=end_date_time.isoformat(timespec='seconds') + "Z"
    )
    return [e for p in pages for e in p]
