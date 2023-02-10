import traci

# Connect to SUMO simulation
# traci.start(["sumo", "-c", "Sumo.sumocfg"])
traci.init(50376)

# Get the list of vehicles in the simulation
vehicle_id="veh0"

# Set the speed of the first vehicle
traci.vehicle.setSpeed(vehicle_id,2)

# Close the connection
traci.close()