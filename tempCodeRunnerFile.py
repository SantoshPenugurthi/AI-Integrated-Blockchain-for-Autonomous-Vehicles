while traci.simulation.getMinExpectedNumber() > 0:
    # Get the data for the current vehicle
    vehicle_data = traci.vehicle.getVehicleData(vehicle_id)

    # Make a decision based on the vehicle data
    make_decision(vehicle_data)

    # Advance the simulation by one step
    traci.simulationStep()