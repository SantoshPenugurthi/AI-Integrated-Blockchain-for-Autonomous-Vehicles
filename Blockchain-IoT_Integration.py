from web3 import Web3, HTTPProvider
import json
import traci
import math

# Connect to the local Ethereum node
w3 = Web3(HTTPProvider('http://localhost:7545'))

# Load the contract ABI
with open('SmartContract.abi') as f:
    abi = json.load(f)

# Load the contract address
with open('address.txt') as f:
    contract_address = f.read()

# Create a contract instance
contract = w3.eth.contract(address=contract_address, abi=abi)


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

    # Update vehicle speed in the blockchain
    for vehicle_id in vehicle_ids:
        print("\n")
        speed = traci.vehicle.getSpeed(vehicle_id)#1
        speed=math.ceil(speed)

        route = traci.vehicle.getRoute(vehicle_id)#2
        route_arr = list(map(str, route))

        current_edge_id = traci.vehicle.getRoadID(vehicle_id)#3
        route_index=traci.vehicle.getRouteIndex(vehicle_id)#4

        if 0 <= route_index < len(route):
            if(current_edge_id!='n5n6'):
                next_edge = route[route_index + 1]#5

        next_edge_vehicles = traci.edge.getLastStepVehicleIDs(next_edge)#6
        remove_obstacles = ("o1", "o2","o3","o4")
        next_edge_vehicles = tuple(filter(lambda x: x not in remove_obstacles, list(next_edge_vehicles)))
        next_edge_vehicles_arr=list(map(str,next_edge_vehicles))

        tx_hash = contract.functions.updateVehicleInfo(vehicle_id, speed,route_arr,current_edge_id,route_index,next_edge,next_edge_vehicles_arr).transact({'from': w3.eth.accounts[0], 'gas': 1000000})
        print('Transaction hash:', tx_hash.hex())

        # Wait for the transaction to be mined
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print('Transaction mined in block', receipt.blockNumber)

        # Retrieve updated vehicle information from blockchain
        speed = contract.functions.getVehicleSpeed(vehicle_id).call()
        print('Speed of vehicle {} : {}'.format(vehicle_id, speed))

        route = contract.functions.getVehicleRoute(vehicle_id).call()
        route=tuple(route)
        print('route of vehicle {} : {}'.format(vehicle_id, route))

        current_edge_id = contract.functions.getVehicleCurrentEdge(vehicle_id).call()
        print('current edge of vehicle {} : {}'.format(vehicle_id, current_edge_id))

        route_index = contract.functions.getVehicleRouteIndex(vehicle_id).call()
        print('route index of vehicle {} : {}'.format(vehicle_id, route_index))

        next_edge = contract.functions.getVehicleNextEdge(vehicle_id).call()
        print('next edge of vehicle {} : {}'.format(vehicle_id, next_edge))

        next_edge_vehicles = contract.functions.getVehicleNextEdgeVehicles(vehicle_id).call()
        next_edge_vehicles=tuple(next_edge_vehicles)
        print('vehicles of next edge of {} : {}'.format(vehicle_id, next_edge_vehicles))
    

    if "veh3" in vehicle_ids:
        print("\n")
        # route = traci.vehicle.getRoute("veh3")#2
        route=contract.functions.getVehicleRoute(vehicle_id).call()
        route=tuple(route)
        print("route of veh3:",route)

        # current_edge_id = traci.vehicle.getRoadID("veh3")#3
        current_edge_id = contract.functions.getVehicleCurrentEdge("veh3").call()
        print("current edge of veh3:",current_edge_id)

        # route_index=traci.vehicle.getRouteIndex("veh3")#4
        route_index = contract.functions.getVehicleRouteIndex("veh3").call()
        print("route index:",route_index)

        if 0 <= route_index < len(route):
            if(current_edge_id!='n5n6'):
                # next_edge = route[route_index + 1]#5
                next_edge = contract.functions.getVehicleNextEdge("veh3").call()
                print("next edge of veh3:", next_edge)

                # vehicle_ids = traci.edge.getLastStepVehicleIDs(next_edge)#6
                # remove_obstacles = ("o1", "o2","o3","o4")
                # vehicle_ids = tuple(filter(lambda x: x not in remove_obstacles, list(vehicle_ids)))
                vehicle_ids = contract.functions.getVehicleNextEdgeVehicles("veh3").call()
                vehicle_ids= tuple(vehicle_ids)

                if(len(vehicle_ids)>0):
                    print("vehicles on edge",next_edge,":",vehicle_ids)
                    speed=0
                    number_of_vehicles=0
                    for id in vehicle_ids:
                        # speed = speed+traci.vehicle.getSpeed(id)#1
                        speed =speed+contract.functions.getVehicleSpeed(id).call()
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


