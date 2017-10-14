//
//  API.swift
//  ColorMeB2C
//
//  Created by Alexander Danilyak on 21/08/2017.
//  Copyright © 2017 Alexander Danilyak. All rights reserved.
//

import Foundation
import Alamofire
import RxSwift
import SwiftyJSON

/// All API availiable to the App
class API {
    
    /// Base URL
    fileprivate let baseUrl: String = "http://hack.ryadom.me/api/"
    
    static let shared: API = API()
    
    let session: SessionManager
    
    private init() {
        let configuration = URLSessionConfiguration.default
        configuration.timeoutIntervalForRequest = 30
        session = Alamofire.SessionManager(configuration: configuration)
    }
    
    fileprivate var headers: [String: String] {
        var h: [String: String] = [:]
        
        if let auth = AuthData.shared.token {
            h["Authorization"] = "Token \(auth)"
        }
        
        return h
    }
    
    func headers(with contentType: String) -> [String: String] {
        var customHeaders = headers
        customHeaders["Content-Type"] = contentType
        return customHeaders
    }

}

// MARK: - Methods
extension API {
    
    func upload(pathComponents: [String],
                fileData: Data,
                name: String,
                fileName: String,
                mimeType: String) -> Observable<JSON> {
        
        return Observable<JSON>.create { [unowned self] observer in
            let appendingMultipartBlock: (MultipartFormData) -> Void = { data in
                data.append(fileData, withName: name, fileName: fileName, mimeType: mimeType)
            }
            
            self.session.upload(multipartFormData: appendingMultipartBlock,
                                usingThreshold: SessionManager.multipartFormDataEncodingMemoryThreshold,
                                to: self.path(with: pathComponents),
                                method: .post,
                                headers: self.headers(with: "multipart/form-data"))
            { result in
                switch result {
                case .success(let request, _, _):
                    request.responseJSON(completionHandler: { dataResponse in
                        guard let response = dataResponse.response else {
                            observer.onError(APIError.lostConnection)
                            return
                        }
                        
                        guard (200..<300).contains(response.statusCode) else {
                            observer.onError(APIError._statusCodeError(response.statusCode, dataResponse.error))
                            return
                        }
                        
                        switch dataResponse.result {
                        case .success(let jsonValue):
                            observer.onNext(JSON(jsonValue))
                        case .failure(let error):
                            observer.onError(error)
                            break
                        }
                    })
                    
                case .failure(let error):
                    observer.onError(APIError.wrongPayloadEncoding(error))
                }
            }
            
            return Disposables.create()
        }
    }
    
    func request(with components: [String], method: HTTPMethod, encoding: ParameterEncoding,  params: [String: Any]?) -> Observable<JSON> {
        return Observable<JSON>.create { [unowned self] observer in
            self.session.request(self.path(with: components),
                                 method: method,
                                 parameters: params,
                                 encoding: encoding,
                                 headers: self.headers(with: "application/json"))
                .responseJSON(completionHandler:
                    { dataResponse in
                        guard let response = dataResponse.response else {
                            observer.onError(APIError.lostConnection)
                            return
                        }
                        
                        guard (200..<300).contains(response.statusCode) else {
                            switch dataResponse.result {
                            case .success(let jsonValue):
                                let error = JSON(jsonValue)
                                observer.onError(APIError._internalDescription(response.statusCode, error.debugDescription))
                            default:
                                observer.onError(APIError._statusCodeError(response.statusCode, dataResponse.error))
                            }
                            return
                        }
                        
                        switch dataResponse.result {
                        case .success(let jsonValue):
                            observer.onNext(JSON(jsonValue))
                        case .failure(let error):
                            observer.onError(error)
                            break
                        }
                })
            
            return Disposables.create()
        }
    }
    
}

private extension API {

    func path(with components: [String]) -> String {
        return baseUrl + components.joined(separator: "/")
    }
    
}
