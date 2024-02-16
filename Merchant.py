from typing import List

import netsquid as ns
from netqasm.sdk.classical_communication.socket import Socket
from netqasm.sdk.connection import BaseNetQASMConnection
from netqasm.sdk.epr_socket import EPRSocket

from squidasm.sim.stack.program import Program, ProgramContext, ProgramMeta

class MerchantPrograme(Program):
    def __init__(self, client: str, bank: str, merchant_id: str):
        self.client = client
        self.bank = bank

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="tutorial_program",
            csockets=[self.client, self.bank],
			epr_sockets=self.client,
            max_qubits=1,
        )
        

    def run(self, context: ProgramContext):
        # get classical socket to peer
        bankCsocket = context.csockets[self.bank]
        clientCsocket = context.csockets[self.client]
        # get connection to quantum network processing unit
        connection = context.connection

        # Merchant listens for messages on his classical socket
        clientMessage = yield from clientCsocket.recv()
        print(f"{ns.sim_time()} ns: Merchant receives from Client message: {clientMessage}")

        messageToBank = clientMessage + merchant_id 
        bankCsocket.send(messageToBank)
        print(f"{ns.sim_time()} ns: Merchant sends to Bank message: {messageToBank}")
    
        connection.flush()

        return {}