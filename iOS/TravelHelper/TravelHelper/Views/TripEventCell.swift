//
//  TripPreviewCell.swift
//  TravelHelper
//
//  Created by Alexander Danilyak on 14/10/2017.
//  Copyright © 2017 Alexander Danilyak. All rights reserved.
//

import UIKit
import Mapbox

class TripEventCell: UICollectionViewCell {
    
    @IBOutlet weak var container: UIView!
    @IBOutlet weak var title: UILabel!
    @IBOutlet weak var detail: UILabel!
    @IBOutlet weak var price: UILabel!
    
}

extension TripEventCell {
    
    func set(event: Event) {
        title.text = event.title
        detail.text = event.detail
        
        switch event {
        case .flight(let data):
            price.text = data.price
            price.isHidden = false
        default:
            price.isHidden = true
            break
        }
    }
    
    override func awakeFromNib() {
        super.awakeFromNib()
        
        title.font = UIHelper.defaultFont(of: 18, weight: .medium)
        title.textColor = UIHelper.tint
        
        detail.font = UIHelper.defaultFont(of: 16, weight: .regular)
        detail.textColor = UIHelper.text
        
        price.font = UIHelper.defaultFont(of: 16, weight: .regular)
        price.textColor = UIHelper.tint
        
        container.layer.cornerRadius = 13.0
        container.layer.borderWidth = 0.5
        container.layer.borderColor = UIHelper.text.withAlphaComponent(0.2).cgColor
    }
    
}
