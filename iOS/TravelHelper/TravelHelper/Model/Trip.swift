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
        case .flight(let data):
            return "Catch a flight from \(data.from) to \(data.to)\n" + place.generateAddress()
        case .arrival(let data):
            return "Welcome to \(data.to)\n" + place.generateAddress()
        case .hotel(let data):
            return "Take a rest at \(data.name)\n" + place.generateAddress()
        case .event(let data):
            return "Join the amazing \(data.performer)\n" + place.generateAddress()
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
            print(json.debugDescription)
            fatalError("Wrong node_type")
        }
    }
    
}

struct FlightData {
    var from: String
    var to: String
    var price: String
    var ticket: URL?
    var carrier: String
    var place: Place
    
    init(json: JSON) {
        self.from = json["from"].stringValue
        self.to = json["to"].stringValue
        self.price = json["price"].stringValue
        self.ticket = json["ticket_uri"].url
        self.carrier = json["carrier"].stringValue
        self.place = Place(json: json["place"])
    }
}

struct ArrivalData {
    var from: String
    var to: String
    var price: String
    var carrier: String
    var place: Place
    
    init(json: JSON) {
        self.from = json["from"].stringValue
        self.to = json["to"].stringValue
        self.price = json["price"].stringValue
        self.carrier = json["carrier"].stringValue
        self.place = Place(json: json["place"])
    }
}

struct HotelData {
    var name: String
    var price: String
    var ticket: URL?
    var place: Place
    
    init(json: JSON) {
        self.name = json["name"].stringValue
        self.place = Place(json: json["place"])
        self.ticket = json["ticket_uri"].url
        self.price = json["price"].stringValue
    }
}

struct EventData {
    var performer: String
    var ticket: URL?
    var place: Place
    
    init(json: JSON) {
        self.performer = json["performer"].stringValue
        self.ticket = json["ticket_uri"].url
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
