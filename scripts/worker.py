from web3 import Web3
import json
from multiprocessing import Process
import random

""" for i in range(0, 10):
    contract.functions.register().transact({"from":accounts[i]})

try:
    while True:
        for event in event_filter.get_new_entries():
            print(f'Worker at address {event.args["worker"]} has been selected...')
except KeyboardInterrupt:
    print("Exiting...") """


def simulate_worker(address):
    # Get contract abi
    f = open('./artifacts/contracts/EventsApp.sol/EventsApp.json')
    data = json.load(f)
    abi = data['abi']
    f.close()

    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    contract_address = Web3.to_checksum_address('0x5fbdb2315678afecb367f032d93f642f64180aa3')
    contract = w3.eth.contract(address=contract_address, abi=abi)
    contract.functions.register().transact({'from':address})
    print(f'{address[:5]} registered to the task!')
    print(f'{address[:5]} listening to events...')

    selection_event_filter = contract.events['Selected'].createFilter(fromBlock='latest')
    end_event_filter = contract.events['TaskEnded'].createFilter(fromBlock='latest')
    

    try:
        while True:
            for event in end_event_filter.get_new_entries():
                print(f'Exiting because task has ended...')
                return
            for event in selection_event_filter.get_new_entries():
                if (address == event.args['worker']):
                    work = [random.randint(0,10) for i in range(5)]
                    print(f'Worker at address {address[:5]} submitting {work}')
                    contract.functions.commitWork(work).transact({"from":address})
    except KeyboardInterrupt:
        print("Exiting...")


if __name__=="__main__":
    
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    accounts = w3.eth.accounts
    processes = []  
    for address in accounts[:len(accounts)-2]:
            p = Process(
                        target = simulate_worker, 
                        args = ([address])
                        )
            p.start()
            processes.append(p)

    for p in processes:
        p.join()