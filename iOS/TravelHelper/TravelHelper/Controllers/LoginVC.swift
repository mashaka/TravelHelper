//
//  LoginVC.swift
//  TravelHelper
//
//  Created by Alexander Danilyak on 14/10/2017.
//  Copyright © 2017 Alexander Danilyak. All rights reserved.
//

import UIKit

class LoginVC: UIViewController {
    
    @IBOutlet weak var loginFacebook: UIButton!
    
}

// MARK: - Actions
extension LoginVC {
    
    @IBAction func onLogin(_ sender: Any) {
        
        Auth.loginToFacebook()
        
    }
    
}
