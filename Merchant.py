from typing import List

import netsquid as ns
from netqasm.sdk.classical_communication.socket import Socket
from netqasm.sdk.connection import BaseNetQASMConnection
from netqasm.sdk.epr_socket import EPRSocket

from squidasm.sim.stack.program import Program, ProgramContext, ProgramMeta

class MerchantProgram(Program):
    def __init__(self, parties: List[str], merchant_id: str):
        self.parties = parties

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="sqdp",
            csockets=self.parties,
			epr_sockets=self.parties,
            max_qubits=128,
        )
    
    def run(self, context: ProgramContext):
        # get classical socket to peer
        bankCsocket = context.csockets[self.parties[1]]
        clientCsocket = context.csockets[self.parties[0]]
        # get connection to quantum network processing unit
        connection = context.connection
		
        print("Merchant program started")

        # Merchant listens for messages on his classical socket
        clientMessage = yield from clientCsocket.recv()
        print(f"{ns.sim_time()} ns: Merchant receives from Client message: {clientMessage}")

        messageToBank = clientMessage + merchant_id 
        bankCsocket.send(messageToBank)
        print(f"{ns.sim_time()} ns: Merchant sends to Bank message: {messageToBank}")
    
        yield from connection.flush()

        return {}