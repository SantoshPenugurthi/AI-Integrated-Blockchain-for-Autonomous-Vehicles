from web3 import Web3, HTTPProvider
import json
import traci

# Connect to the local Ethereum node
w3 = Web3(HTTPProvider('http://localhost:8545'))

# Load the contract ABI
with open('VehicleInfo_sol_VehicleInfo.abi') as f:
    abi = json.load(f)

# Load the contract address
with open('address.txt') as f:
    contract_address = f.read()

# Create a contract instance
contract = w3.eth.contract(address=contract_address, abi=abi)


traci.start(["sumo-gui","-c", "Sumo.sumocfg"])

step=0
veh0_step=0
veh1_step=0

while traci.simulation.getMinExpectedNumber() > 0:
    print("step:", step)
    step=step+1
    traci.simulationStep()
    vehicle_ids = traci.vehicle.getIDList()
    # Update vehicle speed
    for vehicle_id in vehicle_ids:
        new_speed = traci.vehicle.getSpeed(vehicle_id)
        tx_hash = contract.functions.updateVehicleSpeed(vehicle_id, new_speed).transact({'from': w3.eth.accounts[0], 'gas': 100000})
        print('Transaction hash:', tx_hash.hex())

        # Wait for the transaction to be mined
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print('Transaction mined in block', receipt.blockNumber)

        # Retrieve updated vehicle information
        speed = contract.functions.getVehicleInfo(vehicle_id).call()
        print('New speed of vehicle {} is {}.'.format(vehicle_id, speed))

    if "veh0" in vehicle_ids:
        if(traci.vehicle.getRoadID("veh0")=="n2n3" ):
            if(veh0_step<300):
                if(veh0_step==5):
                    traci.vehicle.setSpeed("veh0",0)
            else:
                traci.vehicle.setSpeed("veh0",2)
            veh0_step=veh0_step+1


    if "veh1" in vehicle_ids:
        if(traci.vehicle.getRoadID("veh1")=="n9n10"):
            if(veh1_step<300):
                if(veh1_step==5):
                    traci.vehicle.setSpeed("veh1",0)
            else:
                traci.vehicle.setSpeed("veh1",2)
            veh1_step=veh1_step+1
    

    if "veh3" in vehicle_ids:
        route = traci.vehicle.getRoute("veh3")
        print("Route of veh3",route)

        current_edge_id = traci.vehicle.getRoadID("veh3")
        print("Current edge of veh3:",current_edge_id)

        route_index=traci.vehicle.getRouteIndex("veh3")

        if 0 <= route_index < len(route):
            if(current_edge_id!='n5n6'):
                next_edge = route[route_index + 1]
                print("Next edge of veh3:", next_edge)

                vehicle_ids = traci.edge.getLastStepVehicleIDs(next_edge)
                print("vehicles on edge",next_edge,":",vehicle_ids)

                for id in vehicle_ids:
                    speed = traci.vehicle.getSpeed(id)
                    print("speed of",id,':',speed)

                    if(speed==0 and next_edge=='n2n3'):
                        traci.vehicle.setRoute("veh3",["n1n2","n2n7","n7n8","n8n9", "n9n10", "n10n4", "n4n5", "n5n6"])

                    if(speed==0 and next_edge=='n9n10'):
                        traci.vehicle.setRoute("veh3",["n8n9","n9n3","n3n12","n12n13","n13n14","n14n5","n5n6"])

traci.close()


