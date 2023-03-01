// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SmartContract {
    // Define a struct to represent a vehicle
    struct Vehicle {
        string id;
        uint256 speed;
    }

    // Define a mapping to store vehicle data by ID
    mapping (string => Vehicle) vehicles;

    // Function to retrieve vehicle data by ID
    function getVehicleInfo(string memory id) public view returns (uint256) {
        Vehicle memory vehicle = vehicles[id];
        return (vehicle.speed);
    }

    // Function to update vehicle data by ID
    function updateVehicleInfo(string memory id, uint256 speed) public {
        Vehicle memory vehicle = Vehicle(id, speed);
        vehicles[id] = vehicle;
    }
}