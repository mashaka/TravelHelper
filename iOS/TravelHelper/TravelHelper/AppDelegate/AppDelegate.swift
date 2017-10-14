//
//  AppDelegate.swift
//  TravelHelper
//
//  Created by Alexander Danilyak on 14/10/2017.
//  Copyright © 2017 Alexander Danilyak. All rights reserved.
//

import UIKit

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplicationLaunchOptionsKey: Any]?) -> Bool {
        
        UIHelper.setNavBarAppearance()
        
        return true
    }

    func application(_ application: UIApplication, handleOpen url: URL) -> Bool {
        if url.scheme == "travel" {
            if AuthData.shared.setFromQuery(query: url.query!) {
                DispatchQueue.main.async {
                    Router.getTopMostVisibleController().dismiss(animated: true, completion: {
                        if let tripList = Router.getTopMostVisibleController() as? TripListVC {
                            tripList.loadTrips()
                        }
                        //let chat = Router.getTopMostVisibleController() as! ChatListController
                        //chat.updateAll()
                    })
                }
            }
        }
        return true
    }

}

