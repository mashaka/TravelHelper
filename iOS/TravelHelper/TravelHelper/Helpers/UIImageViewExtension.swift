//
//  UIImageViewExtension.swift
//  ColorMeB2C
//
//  Created by Alexander Danilyak on 31/08/2017.
//  Copyright © 2017 Alexander Danilyak. All rights reserved.
//

import UIKit
import AlamofireImage

fileprivate let imageCache = AutoPurgingImageCache()

fileprivate let imageDownloader = ImageDownloader(configuration: ImageDownloader.defaultURLSessionConfiguration(),
                                                  downloadPrioritization: .lifo,
                                                  maximumActiveDownloads: 4,
                                                  imageCache: imageCache)

extension UIImageView {

    func set(imageUrl: URL) {
        let request = URLRequest(url: imageUrl)
        imageDownloader.download(request) { [weak self] dataResponse in
            guard let `self` = self else {
                return
            }
            
            guard let image = dataResponse.result.value else {
                return
            }
            
            DispatchQueue.main.async {
                UIView.transition(with: self,
                                  duration: 0.2,
                                  options: .transitionCrossDissolve,
                                  animations: {
                                    self.image = image
                }, completion: nil)
            }
            
        }
    }
    
}
