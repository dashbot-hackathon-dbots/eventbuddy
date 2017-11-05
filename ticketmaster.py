import ticketpy


# def find_events(start_date_time, end_date_time, classification_names, latitude, longitude):
tm_client = ticketpy.ApiClient('4KEuLm3GnFY5e8ROVqrn8aUvwUYGO4AL')
pages = tm_client.events.find(
    classification_name='Hip-Hop',
    state_code='GA',
    start_date_time='2017-11-04T20:00:00Z',
    end_date_time='2017-11-10T20:00:00Z'
)

for page in pages:
    for event in page:
        print(event)