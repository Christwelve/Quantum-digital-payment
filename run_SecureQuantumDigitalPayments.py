from application import ClientProgram, ServerProgram
from netsquid_magic.models.perfect import PerfectLinkConfig
from netsquid_netbuilder.modules.clinks.default import DefaultCLinkConfig
from netsquid_netbuilder.util.network_generation import create_complete_graph_network

from squidasm.run.stack.run import run
from Client import ClientPrograme
from Bank import BankPrograme
from Merchant import MerchantPrograme

import os
import base64

node_client_name = "Client"
node_bank_name = "Bank"
node_merchants = ["Merchant1", "Merchant2"]
nodeList = [node_client_name, node_bank_name,node_merchants[0], node_merchants[1]]

# Merchant id should be 128 bit length
merchant_ids = [[merchant, base64.b64encode(os.urandom(16))] for merchant in node_merchants]

lambda_parameter = 128
C = os.urandom(32)

M = [merchant_id[1] for merchant_id in merchant_ids]

# import network configuration from file
cfg = create_complete_graph_network(
    nodeList,
    "perfect",
    PerfectLinkConfig(state_delay=100),
    clink_typ="default",
    clink_cfg=DefaultCLinkConfig(delay=100),
)



programs = {
    node_client_name: ClientPrograme(parties = [node_bank_name] + node_merchants, lambda_parameter=lambda_parameter, C=C, M=M),
    node_bank_name: BankPrograme(client=node_client_name, merchants=node_merchants),
}

for merchant_id in merchant_ids:
    programs[merchant_id[0]] = MerchantPrograme(client=node_client_name, bank=node_bank_name)

# Run the simulation. Programs argument is a mapping of network node labels to programs to run on that node
run(config=cfg, programs=programs, num_times=1)