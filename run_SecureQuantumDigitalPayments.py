from application import ClientProgram, ServerProgram
from netsquid_magic.models.perfect import PerfectLinkConfig
from netsquid_netbuilder.modules.clinks.default import DefaultCLinkConfig
from netsquid_netbuilder.util.network_generation import create_complete_graph_network

from squidasm.run.stack.run import run
from Client import ClientPrograme
from Bank import BankPrograme
from Merchant import MerchantPrograme

node_client_name = "Client"
node_bank_name = "Bank"
node_merchant_name = "Merchant"
nodeList = [node_client_name, node_bank_name,node_merchant_name]

# import network configuration from file
cfg = create_complete_graph_network(
    nodeList,
    "perfect",
    PerfectLinkConfig(state_delay=100),
    clink_typ="default",
    clink_cfg=DefaultCLinkConfig(delay=100),
)


programs = {
    node_client_name: ClientPrograme(bank=node_bank_name, merchant=node_merchant_name)
    node_bank_name: BankPrograme(client=node_client_name, merchant=node_merchant_name)
    node_merchant_name: Merchant(client=node_client_name,bank=node_bank_name)
    }

# Run the simulation. Programs argument is a mapping of network node labels to programs to run on that node
run(config=cfg, programs=programs, num_times=1)
