//
//  TripsListVC.swift
//  TravelHelper
//
//  Created by Alexander Danilyak on 14/10/2017.
//  Copyright © 2017 Alexander Danilyak. All rights reserved.
//

import UIKit
import Mapbox
import SnapKit
import  Hero

class TripTimelineVC: UIViewController {
    
    var trip: Trip!
    
    fileprivate lazy var mapView: MGLMapView = MGLMapView(frame: .zero,
                                                          styleURL: URL(string: "mapbox://styles/hackupc2017travel/cj8rhor043wgc2ro4cx7auv78"))
    
    @IBOutlet weak var eventsCollection: UICollectionView!
    
}

extension TripTimelineVC {
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        mapViewSetup()
        
        eventsCollection.backgroundColor = UIColor.clear
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
    }
    
    func mapViewSetup() {
        if trip.events.count > 0 {
            let c = trip.events[0].coordinates
            mapView.setCenter(CLLocationCoordinate2D(latitude: c.0,
                                                     longitude: c.1),
                              zoomLevel: 9,
                              animated: false)
            
            trip.events.forEach { event in
                let c = event.coordinates
                let annotation = MGLPointAnnotation()
                annotation.coordinate = CLLocationCoordinate2D(latitude: c.0, longitude: c.1)
                annotation.title = event.title
                annotation.subtitle = event.detail
                mapView.addAnnotation(annotation)
            }
        }
        
        mapView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        
        view.insertSubview(mapView, belowSubview: eventsCollection)
        mapView.snp.remakeConstraints { maker in
            maker.edges.equalToSuperview()
        }
    }
    
}

extension TripTimelineVC: UICollectionViewDelegate, UICollectionViewDataSource, UICollectionViewDelegateFlowLayout {
    
    func numberOfSections(in collectionView: UICollectionView) -> Int {
        return 1
    }
    
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return trip.events.count
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        guard let tripCell: TripEventCell = collectionView.dequeueReusableCell(withReuseIdentifier: "tripEventCell", for: indexPath) as? TripEventCell else {
            fatalError("Can't find tripEventCell cell")
        }
        
        tripCell.set(event: trip.events[indexPath.row])
        
        return tripCell
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
        return CGSize(width: collectionView.bounds.width,
                      height: collectionView.bounds.height)
    }
    
    func scrollViewDidEndDecelerating(_ scrollView: UIScrollView) {
        let pageWidth = eventsCollection.frame.size.width
        let currentPage = Int(eventsCollection.contentOffset.x / pageWidth)
        print("PAGE \(currentPage)")
        let c = trip.events[currentPage].coordinates
        mapView.setCenter(CLLocationCoordinate2D(latitude: c.0,
                                                 longitude: c.1),
                          zoomLevel: 9,
                          animated: true)
    }
    
}
