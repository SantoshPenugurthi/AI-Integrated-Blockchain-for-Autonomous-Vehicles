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
        speed = traci.vehicle.getSpeed(vehicle_id)
        speed=math.ceil(speed)
        tx_hash = contract.functions.updateVehicleInfo(vehicle_id, speed).transact({'from': w3.eth.accounts[0], 'gas': 1000000})
        print('Transaction hash:', tx_hash.hex())

        # Wait for the transaction to be mined
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print('Transaction mined in block', receipt.blockNumber)

        # Retrieve updated vehicle information from blockchain
        speed = contract.functions.getVehicleInfo(vehicle_id).call()
        print('Speed of vehicle {} is {}.'.format(vehicle_id, speed))
    

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
                        traci.vehicle.setRoute("veh3",["n8n9","n9n3","n3n12","n12n13","n13n14","n14n5","n5n6"])
                        print("new route of veh3:",traci.vehicle.getRoute("veh3"))
                else:
                    print("vehicles on edge",next_edge,":","No vehicles")

traci.close()


