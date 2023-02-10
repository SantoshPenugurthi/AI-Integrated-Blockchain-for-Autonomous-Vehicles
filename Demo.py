
import traci


traci.start(["sumo-gui","-c", "Sumo.sumocfg"])

step=0
while traci.simulation.getMinExpectedNumber() > 0:
    print("step:", step)
    step=step+1
    traci.simulationStep()

    if(traci.vehicle.getRoadID("veh0")=="n2n3"):
        traci.vehicle.setSpeed("veh0",0)
    if(traci.vehicle.getRoadID("veh1")=="n9n10"):
        traci.vehicle.setSpeed("veh1",0)
    
    
    route = traci.vehicle.getRoute("veh3")
    print("Route of veh3",route)

    current_edge_id = traci.vehicle.getRoadID("veh3")
    print("Current edge of veh3:",current_edge_id)
    # Get the next edge of the vehicle
    route_index=traci.vehicle.getRouteIndex("veh3")

    if 0 <= route_index < len(route):
        if(current_edge_id!='n5n6'):
            next_edge = route[route_index + 1]
        

            # Print the next edge
            print("Next edge of veh3:", next_edge)

            vehicle_ids = traci.edge.getLastStepVehicleIDs(next_edge)

        # Print the list of vehicles on edge "n2n3"
            print("vehicles on edge",next_edge,":",vehicle_ids)

            for id in vehicle_ids:
                speed = traci.vehicle.getSpeed(id)
                print("speed of",id,':',speed)
                if(speed==0 and next_edge=='n2n3'):
                    # traci.vehicle.changeLane("veh0",1,5)
                    traci.vehicle.setRoute("veh3",["n1n2","n2n7","n7n8","n8n9", "n9n10", "n10n4", "n4n5", "n5n6"])
                if(speed==0 and next_edge=='n9n10'):
                    # traci.vehicle.changeLane("veh0",1,5)
                    traci.vehicle.changeLane("veh3",0,20)
                    traci.vehicle.setRoute("veh3",["n8n9","n9n3","n3n12","n12n13","n13n14","n14n5","n5n6"])

traci.close()