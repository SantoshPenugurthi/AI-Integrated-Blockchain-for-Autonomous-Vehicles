import traci

traci.start(["sumo-gui","-c", "Sumo.sumocfg"])

step=0

while traci.simulation.getMinExpectedNumber() > 0:
    print("\nStep:", step,"---------------------------------------------------------------------------->")
    step=step+1
    traci.simulationStep()
    vehicle_ids = traci.vehicle.getIDList()

    for vehicle_id in vehicle_ids:
        speed = traci.vehicle.getSpeed(vehicle_id)
        print("speed of ",vehicle_id," is:",speed)

traci.close()