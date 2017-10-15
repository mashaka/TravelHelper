"""
Copyright 2017, MachineHeads
Author: Maria Sandrikova
Description: Utils
"""
from geopy.distance import great_circle

def flatten_music_events(music_events):
    """
    Change a structure of JSON array

    Args:
        music_events: [{
            "name": "Foo Fighters",
            "events": [{
                "end_time": "2018-03-07T23:59:00-0300",
                "name": "Foo Fighters y Queens Of The Stone Age | Estadio Vélez",
                "id": "275702786271312",
                "start_time": "2018-03-07T19:00:00-0300",
                "place": {
                    "name": "Estadio Vélez",
                    "id": "1601288550083218",
                    "location": {
                        "latitude": -34.63537404966,
                        "zip": "1408",
                        "city": "Buenos Aires",
                        "street": "Av. Juan B. Justo 9200",
                        "country": "Argentina",
                        "longitude": -58.520695048503
                    }
                }
            }]
        }]

    Returns:
        [{
            "name": "Foo Fighters",
            "end_time": "2018-03-07T23:59:00-0300",
            "name": "Foo Fighters y Queens Of The Stone Age | Estadio Vélez",
            "id": "275702786271312",
            "start_time": "2018-03-07T19:00:00-0300",
            "place": {
                "name": "Estadio Vélez",
                "id": "1601288550083218",
                "location": {
                    "latitude": -34.63537404966,
                    "zip": "1408",
                    "city": "Buenos Aires",
                    "street": "Av. Juan B. Justo 9200",
                    "country": "Argentina",
                    "longitude": -58.520695048503
                }
            }
        }]
    """
    events = []
    for band_info in music_events:
        if 'events' in band_info:
            for band_event in band_info['events']:
                events.append(dict(
                    {
                        'performer': band_info['name'],
                        'type': 'music',
                        'cover_url': band_info['cover_url'] if 'cover_url' in band_info else None
                    },
                    **band_event
                ))
    return events

def calc_distance(trip_a, trip_b):
    """ Calculate distance between two locations """
    coords_1 = get_coordinates(trip_a)
    coords_2 = get_coordinates(trip_b)
    return great_circle(coords_1, coords_2).km


def get_coordinates(trip):
    """ Return trip coordinates """
    return trip["locations"][0]["place"]["location"]["latitude"], trip["locations"][0]["place"]["location"]["longitude"]
