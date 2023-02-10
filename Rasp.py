import traci
import random

def make_decision(vehicle_data):
    """Function to make decisions based on other vehicle information"""
    # Extract the relevant information from the vehicle data
    speed = vehicle_data["speed"]
    position = vehicle_data["position"]
    lane = vehicle_data["lane"]

    # Use the information to make a decision
    if speed < 2:
        # If the speed is low, change lanes
        if lane == 0:
            traci.vehicle.changeLane(vehicle_id, 1, 5000)
        elif lane == 1:
            traci.vehicle.changeLane(vehicle_id, 0, 5000)
    else:
        # If the speed is high, maintain the current lane
        pass

    # Randomly decide to accelerate or decelerate
    if random.random() < 0.5:
        traci.vehicle.slowDown(vehicle_id, 10, 5000)
    else:
        traci.vehicle.speedUp(vehicle_id, 10, 5000)

# Connect to the SUMO simulation
traci.start(["sumo-gui", "-c", "Sumo.sumocfg"])

# Get the ID of the vehicle
vehicle_id = "veh0"

# Run the simulation
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    # Get the data for the current vehicle
    vehicle_data = traci.vehicle.getVehicleData(vehicle_id)

    # Make a decision based on the vehicle data
    make_decision(vehicle_data)

    # Advance the simulation by one step

# Close the connection to the SUMO simulation
traci.close()