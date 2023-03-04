// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SmartContract {
    // Define a struct to represent a vehicle
    struct Vehicle {
        string id;
        uint256 speed;
        string current_edge_id;
        uint256 route_index;
        string next_edge;
    }

    // Define a mapping to store vehicle data by ID
    mapping (string => Vehicle) vehicles;

    // Function to retrieve vehicle data by ID
    function getVehicleSpeed(string memory id) public view returns (uint256) {
        Vehicle memory vehicle = vehicles[id];
        return (vehicle.speed);
    }
    function getVehicleCurrentEdge(string memory id) public view returns (string memory) {
        Vehicle memory vehicle = vehicles[id];
        return (vehicle.current_edge_id);
    }
    function getVehicleRouteIndex(string memory id) public view returns (uint256) {
        Vehicle memory vehicle = vehicles[id];
        return (vehicle.route_index);
    }
    function getVehicleNextEdge(string memory id) public view returns (string memory) {
        Vehicle memory vehicle = vehicles[id];
        return (vehicle.next_edge);
    }

    // Function to update vehicle data by ID
    function updateVehicleInfo(string memory id, uint256 speed,string memory current_edge_id ,uint256 route_index,string memory next_edge) public {
        Vehicle memory vehicle = Vehicle(id, speed,current_edge_id, route_index,next_edge);
        vehicles[id] = vehicle;
    }
}