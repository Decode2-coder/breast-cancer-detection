from web3 import Web3
from web3.middleware import geth_poa_middleware
import json

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Load contract
with open("build/contracts/PatientConsent.json") as f:
    contract_data = json.load(f)

abi = contract_data["abi"]
contract_address = Web3.toChecksumAddress(contract_data["networks"]["5777"]["address"])
contract = w3.eth.contract(address=contract_address, abi=abi)

DEFAULT_SENDER = Web3.toChecksumAddress("0xa99323293DF76004aeF39B054D15A68990e59424")

# Write function
def give_patient_consent(patient_address: str):
    addr = Web3.toChecksumAddress(patient_address)
    tx = contract.functions.storeConsent("", True).transact({
        "from": DEFAULT_SENDER,
        "gas": 2000000,
    })
    return w3.eth.wait_for_transaction_receipt(tx)

# Read function
def query_patient_consent(patient_address: str):
    addr = Web3.toChecksumAddress(patient_address)
    return contract.functions.queryConsent(addr).call()
