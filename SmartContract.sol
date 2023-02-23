// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SumoVehicleInfo {
    // Define a struct to represent a vehicle
    struct Vehicle {
        string id;
        uint256 speed;
        uint256 lane;
        uint256 position;
    }

    // Define a mapping to store vehicle data by ID
    mapping (string => Vehicle) vehicles;

    // Function to retrieve vehicle data by ID
    function getVehicleInfo(string memory id) public view returns (uint256, uint256, uint256) {
        Vehicle memory vehicle = vehicles[id];
        return (vehicle.speed, vehicle.lane, vehicle.position);
    }

    // Function to update vehicle data by ID
    function updateVehicleInfo(string memory id, uint256 speed, uint256 lane, uint256 position) public {
        Vehicle memory vehicle = Vehicle(id, speed, lane, position);
        vehicles[id] = vehicle;
    }
}