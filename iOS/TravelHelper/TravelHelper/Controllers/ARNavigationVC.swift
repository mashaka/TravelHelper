//
//  ARNavigationVC.swift
//  TravelHelper
//
//  Created by Alexander Danilyak on 15/10/2017.
//  Copyright © 2017 Alexander Danilyak. All rights reserved.
//

import UIKit
import ARCL
import CoreLocation

class ARnavigationVC: UIViewController {
    
    var sceneLocationView = SceneLocationView()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        sceneLocationView.run()
        
        view.addSubview(sceneLocationView)
        
        let coordinate = CLLocationCoordinate2D(latitude: 51.504571, longitude: -0.019717)
        let location = CLLocation(coordinate: coordinate, altitude: 300)
    }
    
    override func viewDidLayoutSubviews() {
        super.viewDidLayoutSubviews()
        
        sceneLocationView.frame = view.bounds
    }
    
}
