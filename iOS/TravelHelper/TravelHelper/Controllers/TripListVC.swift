//
//  TripListVC.swift
//  TravelHelper
//
//  Created by Alexander Danilyak on 14/10/2017.
//  Copyright © 2017 Alexander Danilyak. All rights reserved.
//

import UIKit
import RxSwift

class TripListVC: UIViewController {
    
    var isFirst: Bool = true
    
    fileprivate var trips: [Trip] = []
    
    @IBOutlet weak var table: UITableView!
    @IBOutlet weak var logOutButton: UIBarButtonItem!
    
    fileprivate let refresh: UIRefreshControl = {
        let r = UIRefreshControl()
        r.tintColor = UIHelper.tint
        return r
    }()
    
    fileprivate var dispose: DisposeBag = DisposeBag()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        table.contentInset = UIEdgeInsets(top: 10.0, left: 0.0, bottom: 0.0, right: 0.0)
        table.estimatedRowHeight = 250.0
        table.register(TripPreviewCell.self,
                       forCellReuseIdentifier: TripPreviewCell.description())
        
        refresh.addTarget(self,
                          action: #selector(onRefresh),
                          for: .valueChanged)
        table.refreshControl = refresh
        
        view.backgroundColor = UIHelper.background
        
        if !Auth.isAuthorized {
            present(UIHelper.createLoginNavController(), animated: false, completion: nil)
        } else {
            loadTrips()
        }
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        //navigationItem.largeTitleDisplayMode = .always
    }
    
    @IBAction func onLogOut(_ sender: Any) {
        AuthData.shared.id = nil
        AuthData.shared.token = nil
        present(UIHelper.createLoginNavController(), animated: false, completion: nil)
    }
    
    func loadTrips() {
        refresh.beginRefreshing()
        dispose = DisposeBag()
        
        print("NOW \(Date())")
        TripsFacade
            .loadTrips()
            .delaySubscription(isFirst ? 0.0 : 3.0, scheduler: MainScheduler.asyncInstance)
            .subscribe(onNext: { [weak self] newTrips in
                print("COMPLETE \(Date())")
                guard let `self` = self else {
                    return
                }
                self.isFirst = false
                self.trips = newTrips
                self.table.reloadData()
                self.refresh.endRefreshing()
            }, onError: { [weak self] error in
                print("ON ERROR \(Date())")
                if let apiError = error as? APIError {
                    switch apiError {
                    case ._statusCodeError(let code, _), ._internalDescription(let code, _):
                        if code == 402 {
                            self?.loadTrips()
                            break
                        } else {
                            self?.refresh.endRefreshing()
                        }
                    default:
                        self?.refresh.endRefreshing()
                        break
                    }
                    print(apiError.localizedDescription)
                } else {
                    self?.refresh.endRefreshing()
                    print(error.localizedDescription)
                }
            })
        .disposed(by: dispose)
    }
    
    @objc func onRefresh() {
        isFirst = true
        trips = []
        table.reloadData()
        loadTrips()
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if let trip = sender as? Trip, let tripTimelineVC = segue.destination as? TripTimelineVC {
            tripTimelineVC.trip = trip
        }
    }
    
}

extension TripListVC: UITableViewDelegate, UITableViewDataSource {
    
    func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return trips.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        guard let cell = table.dequeueReusableCell(withIdentifier: TripPreviewCell.description(),
                                                   for: indexPath) as? TripPreviewCell else {
                                                    fatalError("Can't find TripPreviewCell.description() cell")
        }
        
        cell.set(trip: trips[indexPath.row])
        
        return cell
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        performSegue(withIdentifier: "toTrip", sender: trips[indexPath.row])
    }
    
}
