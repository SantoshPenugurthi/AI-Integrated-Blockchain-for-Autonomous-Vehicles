import traci

traci.start(["sumo-gui","-c", "Sumo.sumocfg"])

step=0
obstacle_step=0

while traci.simulation.getMinExpectedNumber() > 0:
    print("\nStep:", step,"---------------------------------------------------------------------------->")
    step=step+1
    traci.simulationStep()
    vehicle_ids = traci.vehicle.getIDList()
    remove_obstacles = ("o1", "o2","o3","o4")
    vehicle_ids = tuple(filter(lambda x: x not in remove_obstacles, list(vehicle_ids)))

    for vehicle_id in vehicle_ids:
        speed = traci.vehicle.getSpeed(vehicle_id)
        print("speed of ",vehicle_id," is:",speed)

    if(obstacle_step<300):
        traci.vehicle.setSpeed("o1",0)
        traci.vehicle.setSpeed("o2",0)
        traci.vehicle.setSpeed("o3",0)
        traci.vehicle.setSpeed("o4",0)
        traci.vehicle.changeLane("o1", 1,10)
        traci.vehicle.changeLane("o2", 1,10)
    elif(obstacle_step==300):
        traci.vehicle.setSpeed("o1",2)
        traci.vehicle.setSpeed("o2",2)
        traci.vehicle.setSpeed("o3",2)
        traci.vehicle.setSpeed("o4",2)
    obstacle_step=obstacle_step+1

traci.close()