//
//  TripsFacade.swift
//  TravelHelper
//
//  Created by Alexander Danilyak on 14/10/2017.
//  Copyright © 2017 Alexander Danilyak. All rights reserved.
//

import Foundation
import RxSwift
import Alamofire

class TripsFacade {
    
    static func loadTrips() -> Observable<[Trip]> {
        return API.shared.request(with: ["trips"],
                                  method: .get,
                                  encoding: JSONEncoding.default,
                                  params: nil)
            .map { json -> [Trip] in
                return json.arrayValue.map { Trip(json: $0) }
            }
    }
    
}
