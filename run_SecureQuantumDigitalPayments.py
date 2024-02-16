from netsquid_magic.models.perfect import PerfectLinkConfig
from netsquid_netbuilder.modules.clinks.default import DefaultCLinkConfig
from netsquid_netbuilder.util.network_generation import create_complete_graph_network

from squidasm.run.stack.run import run
from Client import ClientProgram
from Bank import BankProgram
from Merchant import MerchantProgram

import os
import base64

node_client_name = "Client"
node_bank_name = "Bank"
node_merchant_name = "Merchant1"
nodeList = [node_client_name, node_bank_name,node_merchant_name]
print(nodeList)

# Merchant id should be 128 bit length
#merchant_ids = [[merchant, base64.b64encode(os.urandom(16))] for merchant in node_merchants]
merchant_id = base64.b64encode(os.urandom(16))
lambda_parameter = 128
C = os.urandom(32)

M = [merchant_id]

# import network configuration from file
cfg = create_complete_graph_network(
    nodeList,
    "perfect",
    PerfectLinkConfig(state_delay=100),
    clink_typ="default",
    clink_cfg=DefaultCLinkConfig(delay=100),
)



programs = {
    node_client_name: ClientProgram(parties = [node_bank_name] + [node_merchant_name], lambda_parameter=lambda_parameter, C=C, M=M, client_name=node_client_name),
    node_bank_name: BankProgram(parties=[node_client_name] + [node_merchant_name], lambda_parameter=lambda_parameter, C=C),
	node_merchant_name: MerchantProgram(parties = [node_client_name] + [node_bank_name], merchant_id = M[0])
}

#for merchant_id in merchant_ids:
#    programs[merchant_id[0]] = MerchantProgram(parties = [node_client_name] + [node_bank_name], merchant_id = M[0])

# Run the simulation. Programs argument is a mapping of network node labels to programs to run on that node
run(config=cfg, programs=programs, num_times=1)