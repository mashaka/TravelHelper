import json

import time

from algo import generate_trips
import requests

from config.settings import SKYSCANNER_KEY, SKYSCANNER_KEY_HOTELS
from skyscanner.skyscanner import FlightsCache, Hotels
from dateutil import parser


SKYSCANNER_SETTINGS = {
    'country': 'UK',
    'currency': 'EUR',
    'locale': 'en-GB'
}


def get_city_code(name):
    r = requests.get(
        'http://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/{country}/{currency}/{locale}?query={q}&apiKey={key}'.format(
            **SKYSCANNER_SETTINGS,
            q=name,
            key=SKYSCANNER_KEY)).json()
    return r['Places'][0]['CityId']


def get_city_id(name):
    r = requests.get(
        'http://gateway.skyscanner.net/autosuggest/v3/hotels?q={q}&market={market}&locale={locale}&apiKey={key}'.format(
            locale=SKYSCANNER_SETTINGS['locale'],
            market='UK',
            q=name,
            key=SKYSCANNER_KEY_HOTELS)).json()
    return r['results'][0]['id']


def find_flight(date, fr, to):
    fr = get_city_code(fr)
    to = get_city_code(to)
    api = FlightsCache(SKYSCANNER_KEY)
    data = api.get_cheapest_quotes(**SKYSCANNER_SETTINGS, originplace=fr, destinationplace=to, market='UK',
                                   outbounddate=date, inbounddate='', adults=1).parsed
    carriers = {x['CarrierId']: x['Name'] for x in data['Carriers']}
    places = {x['PlaceId']: x['CityName'] + ', ' + x['IataCode'] for x in data['Places']}
    return [{
        'from': places[q['OutboundLeg']['OriginId']],
        'to': places[q['OutboundLeg']['DestinationId']],
        'price': str(q['MinPrice']) + ' ' + data['Currencies'][0]['Symbol'],
        'ticket_uri': 'http://partners.api.skyscanner.net/apiservices/referral/v1.0/{country}/{currency}/{locale}/{originplace}/{destinationplace}/{outbounddate}/{inbounddate}?apiKey={api}'.format(
            **SKYSCANNER_SETTINGS, originplace=fr, destinationplace=to,
            outbounddate=date, inbounddate='', api=SKYSCANNER_KEY[:16]
        ),
        'carrier': carriers[q['OutboundLeg']['CarrierIds'][0]] if len(q['OutboundLeg']['CarrierIds']) else '',
    } for q in data['Quotes']]


def flight_events(date, fr, to):
    d = find_flight(date, fr['location']['city'], to['location']['city'])
    flight = dict(d[0])
    arrival = dict(d[0])
    flight['node_type'] = 'flight'
    arrival['node_type'] = 'arrival'
    flight['place'] = fr
    arrival['place'] = to
    return [flight, arrival]


def convert_date(date):
    return parser.parse(date).strftime("%Y-%m-%d")


def find_hotel(location):
    data = {'meta': {'status': 'PENDING'}}
    while data['meta']['status'] != 'COMPLETED':
        data = requests.get('https://gateway.skyscanner.net/hotels/v1/prices/search/location/{lon},{lat}?market={market}&locale={locale}&checkin_date={checkin}&checkout_date={checkout}&currency={currency}&adults=1&rooms=1&apikey={key}'.format(
            **SKYSCANNER_SETTINGS,
            lon=location['place']['location']['longitude'],
            lat=location['place']['location']['latitude'],
            market='UK',
            checkin=convert_date(location['start_date']),
            checkout=convert_date(location['end_date']),
            key=SKYSCANNER_KEY_HOTELS,
        ), headers={'x-user-agent': 'T;B2B'}).json()
        time.sleep(1)
    return [{
            'name': x['name'],
            'ticket_uri': 'http://' + x['offers'][0]['deeplink'],
            'price': str(x['offers'][0]['price']) + ' €',
            'stars': x['stars'],
            'node_type': 'hotel',
            'place': location['place'],
            'start_date': location['start_date'],
            'end_date': location['end_date'],
        } for x in data['results']['hotels']
    ]


def process_trip(hometown, trip):
    events = flight_events(convert_date(trip['locations'][0]['start_date']), hometown, trip['locations'][0]['place'])

    for i in range(len(trip['locations'])):
        if i > 0:
            events.extend(
                flight_events(convert_date(trip['locations'][i]['start_date']), trip['locations'][i - 1]['place'],
                              trip['locations'][i]['place']))
        events.append(find_hotel(trip['locations'][i])[0])
        e = [dict(t) for t in trip['locations'][i]['events']]
        for x in e:
            x['node_type'] = 'event'
        events.extend(e)

    events.extend(
        flight_events(convert_date(trip['locations'][-1]['end_date']), trip['locations'][-1]['place'], hometown))
    return {
        'name': trip['name'],
        'reason': trip['reason'],
        'cover_url': trip['cover_url'],
        'events': events
    }


COVERS = {
    'states': 'http://www.nationalgeographic.com/content/dam/travel/photos/000/065/6516.adapt.1900.1.jpg',
    'kingdom': 'http://www.nationalgeographic.com/content/dam/travel/photos/000/123/12369.adapt.1900.1.jpg',
    'argentina': 'http://www.nationalgeographic.com/content/dam/travel/photos/000/075/7500.adapt.1900.1.jpg',
    'ireland': 'http://www.nationalgeographic.com/content/dam/travel/photos/000/060/6017.adapt.1900.1.jpg',
    'brazil': 'http://www.nationalgeographic.com/content/dam/travel/photos/000/066/6647.adapt.1900.1.jpg',
    'emirates': 'https://inassets1-internationsgmbh.netdna-ssl.com/image/static_2048_1152/static/bundles/internationsseo/frontend/images/countryHeroV2/uae.jpg',
}


def change_cover(trip):
    for country, url in COVERS.items():
        if country in trip['name'].lower():
            trip['cover_url'] = url
    return trip


def process(base_info, music_info):
    trips = generate_trips(base_info, music_info)
    trips = list(map(change_cover, trips))
    res = []
    for trip in trips:
        try:
            res.append(process_trip(base_info['hometown'], trip))
        except Exception as e:
            pass
    return res
