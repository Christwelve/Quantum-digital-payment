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
# Merhant id should be 128 bit length
mid1 = os.urandom(16)
mid2 = os.urandom(16)
M = [base64.b64encode(mid1), base64.b64encode(mid2)]

lambda_parameter = 128
C = os.urandom(32)



# import network configuration from file
cfg = create_complete_graph_network(
    nodeList,
    "perfect",
    PerfectLinkConfig(state_delay=100),
    clink_typ="default",
    clink_cfg=DefaultCLinkConfig(delay=100),
)


programs = {
    node_client_name: ClientPrograme(parties = [node_bank_name, node_merchants[0], node_merchants[1]], lambda_parameter=lambda_paramnter, C=C, M=M),
    node_bank_name: BankPrograme(client=node_client_name, merchant=node_merchant_name),
    node_merchant_name: Merchant(client=node_client_name,bank=node_bank_name)
    }

# Run the simulation. Programs argument is a mapping of network node labels to programs to run on that node
run(config=cfg, programs=programs, num_times=1)
