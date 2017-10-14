//
//  UIHelper.swift
//  TravelHelper
//
//  Created by Alexander Danilyak on 14/10/2017.
//  Copyright © 2017 Alexander Danilyak. All rights reserved.
//

import UIKit

class UIHelper {
    
    static let mainStoryboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
    
    static func createLoginNavController() -> UIViewController {
        let loginNav: UIViewController = mainStoryboard.instantiateViewController(withIdentifier: "loginNavVC")
        loginNav.modalTransitionStyle = .flipHorizontal
        return loginNav
    }
    
    // ----------------------------------
    
    static let tint = UIColor(red: 86.0 / 255.0,
                              green: 60.0/255.0,
                              blue: 238.0/255.0,
                              alpha: 1.0)
    
    static let textTitle = UIColor(red: 70.0 / 255.0,
                                   green: 63.0/255.0,
                                   blue: 105.0/255.0,
                                   alpha: 1.0)
    
    static let text = UIColor(red: 87.0 / 255.0,
                              green: 97.0/255.0,
                              blue: 100.0/255.0,
                              alpha: 1.0)
    
    static let background = UIColor(red: 245.0 / 255.0,
                                    green: 245.0/255.0,
                                    blue: 245.0/255.0,
                                    alpha: 1.0)
    
    // ----------------------------------
    
    static func defaultFont(of size: CGFloat = 18.0, weight: UIFont.Weight = .regular) -> UIFont {
        var name: String
        switch weight {
        case .regular:
            name = "Lato-Regular"
        case .medium:
            name = "Lato-Medium"
        default:
            name = "Lato-Regular"
        }
        return UIFont(name: name,
                      size: size)!
    }
    
    // ----------------------------------
    
    static func setNavBarAppearance() {
        
        let navAppearance = UINavigationBar.appearance()
        navAppearance.tintColor = tint
        
        navAppearance.largeTitleTextAttributes = [NSAttributedStringKey.foregroundColor: textTitle,
                                                  NSAttributedStringKey.font: defaultFont(of: 30, weight: .regular)]
        navAppearance.titleTextAttributes = [NSAttributedStringKey.foregroundColor: textTitle,
                                             NSAttributedStringKey.font: defaultFont(of: 20, weight: .regular)]
        
        //navAppearance.shadowImage = UIImage()
        //navAppearance.setBackgroundImage(UIImage(), for: .any, barMetrics: .default)
        
        UIBarButtonItem
            .appearance()
            .setTitleTextAttributes([NSAttributedStringKey.foregroundColor: tint,
                                     NSAttributedStringKey.font: UIFont(name: "Lato-Regular", size: 16.0)!], for: .normal)
    }
    
}
