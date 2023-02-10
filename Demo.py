
import traci

# contains TraCI control loop
def run():
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        current_edge_id = traci.vehicle.getRoadID("veh0")
        print(current_edge_id)
        if(current_edge_id=="n1n2"):
            traci.vehicle.changeLane("veh0",1,5)
            traci.vehicle.setSpeed("veh0",2.0)
            # traci.vehicle.setRoute("veh0",["n1n2","n2n7","n7n8","n8n9", "n9n10", "n10n4", "n4n5", "n5n6"])

    traci.close()

# main entry point
if __name__ == "__main__":

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start(["sumo-gui","-c", "Sumo.sumocfg"])
    run()