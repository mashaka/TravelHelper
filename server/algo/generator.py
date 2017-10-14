"""
Copyright 2017, MachineHeads
Author: Maria Sandrikova
Description: Entry point for package containing main trips generation routine
"""
import json
import logging
import algo.config as config

MODULE_LOGGER = logging.getLogger('generator')

def generate_trips(basic_info, music_info):
    """
    Generate trips

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
    # TODO
    with open(config.MOCK_TRIPS_FILE) as json_file:
        trips = json.load(json_file)
    return trips
