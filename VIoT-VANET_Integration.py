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
    

    if "veh3" in vehicle_ids:
        route = traci.vehicle.getRoute("veh3")
        print("route of veh3:",route)

        current_edge_id = traci.vehicle.getRoadID("veh3")
        print("current edge of veh3:",current_edge_id)

        route_index=traci.vehicle.getRouteIndex("veh3")

        if 0 <= route_index < len(route):
            if(current_edge_id!='n5n6'):
                next_edge = route[route_index + 1]
                print("next edge of veh3:", next_edge)

                vehicle_ids = traci.edge.getLastStepVehicleIDs(next_edge)
                remove_obstacles = ("o1", "o2","o3","o4")
                vehicle_ids = tuple(filter(lambda x: x not in remove_obstacles, list(vehicle_ids)))

                if(len(vehicle_ids)>0):
                    print("vehicles on edge",next_edge,":",vehicle_ids)
                    speed=0
                    number_of_vehicles=0
                    for id in vehicle_ids:
                        speed = speed+traci.vehicle.getSpeed(id)
                        number_of_vehicles=number_of_vehicles+1
                    print("Total speed on road",next_edge,":",speed)
                    print("Number of vehicles on road",next_edge,":",number_of_vehicles)
                    print("Average speed on road",next_edge,':',speed/number_of_vehicles)

                    if(speed==0 and next_edge=='n2n3'):
                        traci.vehicle.setRoute("veh3",["n1n2","n2n7","n7n8","n8n9", "n9n10", "n10n4", "n4n5", "n5n6"])
                        print("new route of veh3:",traci.vehicle.getRoute("veh3"))

                    if(speed==0 and next_edge=='n9n10'):
                        traci.vehicle.setRoute("veh3",["n8n9","n9n3","n3n4","n4n5","n5n6"])
                        print("new route of veh3:",traci.vehicle.getRoute("veh3"))
                else:
                    print("vehicles on edge",next_edge,":","No vehicles")
                

traci.close()