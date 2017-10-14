//
//  TripPreviewCell.swift
//  TravelHelper
//
//  Created by Alexander Danilyak on 14/10/2017.
//  Copyright © 2017 Alexander Danilyak. All rights reserved.
//

import UIKit
import SnapKit
import Mapbox
import Hero

class TripPreviewCell: UITableViewCell {
    
    fileprivate var tripImage: UIImageView = {
        let image = UIImageView()
        image.contentMode = .scaleAspectFill
        image.backgroundColor = UIColor.lightGray
        image.layer.masksToBounds = true
        return image
    }()
    
    fileprivate var container: UIView = UIView()
    
    fileprivate var title: UILabel = {
        let label = UILabel()
        label.font = UIHelper.defaultFont(of: 18, weight: .medium)
        label.textColor = UIHelper.textTitle
        return label
    }()
    
    fileprivate var detail: UILabel = {
        let label = UILabel()
        label.font = UIHelper.defaultFont(of: 16, weight: .regular)
        label.textColor = UIHelper.text
        label.numberOfLines = 0
        return label
    }()
    
    override init(style: UITableViewCellStyle, reuseIdentifier: String?) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)
        
        backgroundColor = UIColor.clear
        
        contentView.addSubview(container)
        container.addSubview(tripImage)
        container.addSubview(title)
        container.addSubview(detail)
        
        container.snp.remakeConstraints { maker in
            maker.edges.equalToSuperview().inset(UIEdgeInsets(top: 10.0,
                                                              left: 20.0,
                                                              bottom: 10.0,
                                                              right: 20.0))
        }
        
        tripImage.snp.remakeConstraints { maker in
            maker.left.top.right.equalToSuperview()
            maker.height.equalTo(200.0)
            maker.bottom.equalTo(title.snp.top).offset(-16.0)
        }
        
        title.snp.remakeConstraints { maker in
            maker.left.right.equalToSuperview().inset(16.0)
            maker.bottom.equalTo(detail.snp.top)
        }
        
        detail.snp.remakeConstraints { maker in
            maker.left.right.equalToSuperview().inset(16.0)
            maker.bottom.equalToSuperview().inset(16.0)
        }
        
        container.layer.cornerRadius = 13.0
        container.layer.masksToBounds = true
        container.backgroundColor = UIColor.white
        
        container.layer.borderWidth = 0.5
        container.layer.borderColor = UIHelper.text.withAlphaComponent(0.2).cgColor
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    func set(trip: Trip) {
        self.title.text = trip.name
        self.detail.text = trip.reason
        if let url = trip.cover {
            self.tripImage.set(imageUrl: url)
        }
    }
    
    
}
