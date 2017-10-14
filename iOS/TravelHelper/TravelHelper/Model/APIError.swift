//
//  APIError.swift
//  ColorMeB2C
//
//  Created by Alexander Danilyak on 22/08/2017.
//  Copyright © 2017 Alexander Danilyak. All rights reserved.
//

import Foundation

enum APIError {
    case lostConnection
    case wrongPayloadEncoding(Error?)
    case _statusCodeError(Int, Error?)
    case _internalDescription(Int, String)
}

extension APIError: Error {}

extension APIError: Localizable {
    
    func text() -> String {
        switch self {
        case .lostConnection:
            return "Connection was lost"
        case .wrongPayloadEncoding:
            return "Encoding Error"
        case ._statusCodeError(let code, let error):
            return "ERROR CODE: \(code)\nERROR DESC: \(error?.localizedDescription ?? "NONE")"
        case ._internalDescription(let code, let description):
            return "ERROR CODE: \(code)\nERROR DESC: \(description)"
        }
    }
    
}

/// Protocol for describing objects (mostly errors)
protocol Localizable {
    
    func text() -> String
    
}
