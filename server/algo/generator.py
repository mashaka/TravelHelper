"""
Copyright 2017, MachineHeads
Author: Maria Sandrikova
Description: Entry point for package containing main trips generation routine
"""
import json
import logging
import uuid
from dateutil import parser
import random
from datetime import datetime, timedelta

import algo.config as config
from algo.user_info import UserInfo

MODULE_LOGGER = logging.getLogger('generator')

def generate_trips(basic_info, music_info):
    """
    Entry point of a trip generation routine

    Args:
        basic_info (JSON): basic user info + posts + tagged places fron user's Facebook page
        music_info: user's favourite music bands and corresponding upcoming events

    Returns:
        [{
            '_id': "000000000",
            'name': USA & One Direction,
            'reason': "There will be a concert of One Direction in this time",
            'cover_url': "http://www.nationalgeographic.com/content/dam/travel/photos/000/000/5.ngsversion.0.adapt.1900.1.jpg",
            'locations': [{
                'start_date': "2015-12-01T19:30:00-0600",
                'end_date': "2015-12-01T19:30:00-0600",
                "place": {
                    "name": "American Airlines Center",
                    "location": {
                        "city": "Dallas",
                        "country": "United States",
                        "latitude": 32.790485550848,
                        "longitude": -96.810278349053,
                        "state": "TX",
                        "street": "2500 Victory Ave",
                        "zip": "75219"
                    },
                    "id": "26606856232"
                },
                'events': [{
                    "type": ("music")
                    "place": {
                        "name": "American Airlines Center",
                        "location": {
                            "city": "Dallas",
                            "country": "United States",
                            "latitude": 32.790485550848,
                            "longitude": -96.810278349053,
                            "state": "TX",
                            "street": "2500 Victory Ave",
                            "zip": "75219"
                        },
                        "id": "26606856232"
                    },
                    "performer": "One Direction",
                    "cover_url": "https://scontent.xx.fbcdn.net/v/t1.0-9/s720x720/12299339_991873664200761_5875457788740586106_n.png?oh=c7f400dee847f410c3bc34ed135fe278&oe=5A782C59",
                    "name": "iHeartRadio Jingle Ball",
                    "start_time": "2015-12-01T19:30:00-0600",
                    "id": "1500891070238980"
                }]
            }]
        }]
    """
    # Parse input data
    user_info = UserInfo(basic_info, music_info)
    # Construct trips
    trips = construct_trips(user_info)
    MODULE_LOGGER.info(
        'Constructed %d trips',
        len(trips)
    )
    return trips


def construct_trips(user_info):
    """
    Main routine generating trips

    Args:
        user_info: UserInfo

    Returns:
        See what generate_trips() returns
    """
    # Filter events
    user_info.set_events(filter_events(user_info.get_events()))
    # Contruct trips from events
    trips = construct_trips_from_events(user_info.get_events())
    # Add cities to trips
    # TODO
    return trips


def construct_trips_from_events(events):
    """ Wrap events in trips with one location """
    trips = []
    for event in events:
        trips.append({
            "_id": str(uuid.uuid1()),
            "name": generate_trip_name(event),
            "reason": generate_trip_reason(event),
            "cover_url": generate_trip_cover(event),
            "locations": [{
                "start_date": generate_start_date(event),
                "end_date": generate_end_date(event),
                "place": event['place'],
                "events": [event]
            }]
        })
    return trips


def check_event_start(event):
    """ Filter events in the past, shich will happen too soon or on the distant future """
    if 'start_time' not in event:
        return False
    start_date = parser.parse(event["start_time"]).date()
    today = datetime.today().date()
    if start_date < today:
        return False
    if (start_date - today).days < config.MIN_DAYS_BEFORE_TRIP:
        return False
    if (start_date - today).days > config.MAX_DAYS_BEFORE_TRIP:
        return False
    return True


def filter_events(events):
    """ Filter events """
    # Filter events without "place" attribute
    filtered_events = [event for event in events if 'place' in event]
    # Filter events without country or city
    filtered_events = [event for event in filtered_events if 'location' in event['place']]
    filtered_events = [event for event in filtered_events if 'country' in event['place']['location']]
    filtered_events = [event for event in filtered_events if 'city' in event['place']['location']]
    # Filter events in the past, shich will happen too soon or on the distant future
    filtered_events = [event for event in filtered_events if check_event_start(event)]
    # Filter too many events of one band
    filtered_events = filter_band_worls_tours(filtered_events)
    return filtered_events


def filter_band_worls_tours(events):
    """ Filter too many events of one band """
    bands = set()
    for event in events:
        bands.add(event["performer"])
    filtered_trips = []
    for band in bands:
        band_events = [event for event in events if event["performer"] == band]
        if len(band_events) > 2:
            filtered_trips.extend(random.sample(band_events, 2))
        else:
            filtered_trips.extend(band_events)
    return filtered_trips


def generate_trip_name(event):
    """ Generate a name for a trip """
    name = "{} & {}".format(event["place"]["location"]["country"], event["performer"])
    return name


def generate_trip_reason(event):
    """ Generate a trip reason """
    reason = "{} will give a contert in {}, {} soon. It is great reason to travel ;)".format(
        event["performer"],
        event["place"]["location"]["city"],
        event["place"]["location"]["country"]
    )
    return reason


def generate_trip_cover(event):
    """ Create a cover for the trip """
    # TODO
    return "https://www.askideas.com/media/23/Very-Cute-Little-Beagle-Puppy-Laying-Down.jpg"


def generate_start_date(event):
    """ Give enough time before the event """
    start_date = parser.parse(event["start_time"]).date() - timedelta(days=config.GAP_BEFORE_EVENT)
    return str(start_date)


def generate_end_date(event):
    """ Add some time after event to see a town """
    end_date = parser.parse(event["start_time"]).date() + timedelta(days=config.GAP_AFTER_EVENT)
    return str(end_date)
