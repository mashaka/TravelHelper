"""
Copyright 2017, MachineHeads
Author: Maria Sandrikova
Description: Entry point for package containing main trips generation routine
"""
import json
import logging
import uuid
import operator
import sys
from dateutil import parser
import random
from datetime import datetime, timedelta

import algo.config as config
from algo.user_info import UserInfo
from algo.utils import calc_distance

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
    # Concatenate trips together
    complex_trips = construct_complex_trips(trips)
    # Filter too many events of one band
    trips = filter_band_worls_tours(trips)
    trips.extend(complex_trips)
    return trips


def construct_complex_trips(trips):
    """ Concatenate trips in complex ones """
    distance_table = [[sys.maxsize for _ in range(len(trips))] for _ in range(len(trips))]
    for first_index, first_trip in enumerate(trips):
       for second_index, second_trip in enumerate(trips):
            if second_index <= first_index:
                continue
            dist = calc_distance(first_trip, second_trip)
            distance_table[first_index][second_index] = dist
            distance_table[second_index][first_index] = dist
    complex_trips = []
    for ind, trip in enumerate(trips): 
        min_index, min_value = min(enumerate(distance_table[ind]), key=operator.itemgetter(1))
        if min_value > config.MAX_DISTANCE_BETWEEN_PLACES:
            continue
        if is_concatenatable(trip, trips[min_index]):
            complex_trips.append(concatenate_trips(trip, trips[min_index]))
        elif is_concatenatable(trips[min_index], trip):
            complex_trips.append(concatenate_trips(trips[min_index], trip))
        comp_min_index, _ = min(enumerate(distance_table[min_index]), key=operator.itemgetter(1))
        if comp_min_index == ind:
            distance_table[min_index][ind] = sys.maxsize
    return complex_trips


def is_concatenatable(trip_a, trip_b):
    """ Check amount of days between trips """
    trip_a_end = parser.parse(trip_a["locations"][0]["end_date"]).date()
    trip_b_start = parser.parse(trip_b["locations"][0]["start_date"]).date()
    if (trip_b_start - trip_a_end).days > config.MAX_GAP_BETWEEN_TRIPS:
        return False
    if (trip_b_start - trip_a_end).days <= 0:
        return False
    if trip_a["locations"][0]["events"][0]["performer"] == trip_a["locations"][0]["events"][0]["performer"]:
        return False
    return True


def concatenate_trips(trip_a, trip_b):
    """ Concatenate information about two trips """
    united_trip = {
        "name": "{} & {}".format(trip_a["name"], trip_b["name"]),
        "reason": generate_united_trip_reason(
            trip_a["locations"][0]["events"][0], 
            trip_b["locations"][0]["events"][0]
        ),
        "cover_url": trip_a["cover_url"],
        "locations": trip_a["locations"] + trip_b["locations"],
    }
    united_trip["locations"][1]["start_date"] = united_trip["locations"][0]["end_date"]
    return united_trip


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
    for filter_keyword in ['country', 'city', 'latitude', 'longitude']:
        filtered_events = [event for event in filtered_events if filter_keyword in event['place']['location']]
    # Filter events in the past, shich will happen too soon or on the distant future
    filtered_events = [event for event in filtered_events if check_event_start(event)]
    return filtered_events


def filter_band_worls_tours(trips):
    """ Filter too many events of one band """
    bands = set()
    for trip in trips:
        bands.add(trip["locations"][0]["events"][0]["performer"])
    filtered_trips = []
    for band in bands:
        band_trips = [trip for trip in trips if trip["locations"][0]["events"][0]["performer"] == band]
        if len(band_trips) > 2:
            filtered_trips.extend(random.sample(band_trips, 2))
        else:
            filtered_trips.extend(band_trips)
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

def generate_united_trip_reason(event_a, event_b):
    """ Generate a trip reason """
    reason = "{} and {} will give a conterts soon. Let's travel! :)".format(
        event_a["performer"],
        event_b["performer"]
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
