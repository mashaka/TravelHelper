//
//  Trip.swift
//  TravelHelper
//
//  Created by Alexander Danilyak on 14/10/2017.
//  Copyright © 2017 Alexander Danilyak. All rights reserved.
//

import Foundation
import SwiftyJSON

struct Trip {
    
    var name: String
    var reason: String
    var cover: URL?
    var events: [Event]
 
    init(json: JSON) {
        self.name = json["name"].stringValue
        self.reason = json["reason"].stringValue
        self.cover = json["cover_url"].url
        self.events = json["events"].arrayValue.map { Event.create(json: $0) }
    }
    
}

enum Event {
    case flight(FlightData)
    case arrival(ArrivalData)
    case hotel(HotelData)
    case event(EventData)
    
    var coordinates: (Double, Double) {
        return (place.latitude, place.longitude)
    }
    
    var title: String {
        switch self {
        case .flight:
            return "✈️  Flight"
        case .arrival:
            return "🎉  Welcome"
        case .hotel:
            return "🏨  Hotel"
        case .event:
            return "🎸  Event"
        }
    }
    
    var detail: String {
        switch self {
        case .flight:
            return "Catch a flight from *airport name* to *airport name*\n" + place.generateAddress()
        case .arrival:
            return "Welcome to *city name*\n" + place.generateAddress()
        case .hotel:
            return "Take a rest at *hotel name*\n" + place.generateAddress()
        case .event:
            return "Be a part of the amazing *event name*\n" + place.generateAddress()
        }
    }
    
    var place: Place {
        switch self {
        case .flight(let data):
            return data.place
        case .arrival(let data):
            return data.place
        case .hotel(let data):
            return data.place
        case .event(let data):
            return data.place
        }
    }
    
    static func create(json: JSON) -> Event {
        let incomingKey = json["node_type"].stringValue
        switch incomingKey {
        case "flight":
            return .flight(FlightData(json: json))
        case "arrival":
            return .arrival(ArrivalData(json: json))
        case "hotel":
            return .hotel(HotelData(json: json))
        case "event":
            return .event(EventData(json: json))
        default:
            fatalError("Wrong node_type")
        }
    }
    
}

struct FlightData {
    var place: Place
    
    init(json: JSON) {
        self.place = Place(json: json["place"])
    }
}

struct ArrivalData {
    var place: Place
    
    init(json: JSON) {
        self.place = Place(json: json["place"])
    }
}

struct HotelData {
    var place: Place
    
    init(json: JSON) {
        self.place = Place(json: json["place"])
    }
}

struct EventData {
    var place: Place
    
    init(json: JSON) {
        self.place = Place(json: json["place"])
    }
}

struct Place {
    
    var name: String
    var country: String?
    var city: String?
    var street: String?
    
    var longitude: Double
    var latitude: Double
    
    init(json: JSON) {
        self.name = json["name"].stringValue
        self.country = json["location"]["country"].string
        self.city = json["location"]["city"].string
        self.street = json["location"]["street"].string
        self.longitude = json["location"]["longitude"].doubleValue
        self.latitude = json["location"]["latitude"].doubleValue
    }
    
    func generateAddress() -> String {
        return [country, city, name, street].flatMap { $0 }.joined(separator: ", ")
        
    }
    
}
