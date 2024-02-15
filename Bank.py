from typing import List
import string
import secrets
import netsquid as ns
from netqasm.sdk.classical_communication.socket import Socket
from netqasm.sdk.connection import BaseNetQASMConnection
from netqasm.sdk.epr_socket import EPRSocket

from squidasm.sim.stack.program import Program, ProgramContext, ProgramMeta

class BankPrograme(Program):
    def __init__(self, client_name: str, merchant_name: str):
        self.client = client_name
        self.merchant = merchant_name

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="sqdp_program",
            csockets=self.client,
            epr_sockets=self.client,
            msockets=self.merchant,
            max_qubits=1,
        )

	def generate_random_string(lenght = 256):
		letters = string.ascii_letters + string.digits
		random_string = ''.join(secrets.choice(letters) for i in range(lenght))
		return random_string

    def run(self, context: ProgramContext):
        connection: BaseNetQASMConnection = context.connection

        #client side
        
        # get classical socket to peer
        csocket: Socket = context.csockets[client]
        epr_socket: EPRSocket = context.epr_sockets[client]

        # send a string message via a classical channel
        # generate C and fix
		C = generate_random_string(256)
        csocket.send(C)
        print(f"{ns.sim_time()} ns: Server sends message: {C}")

        # Register a request to create an EPR pair, then apply a Hadamard gate on the epr qubit and measure
        epr_qubit = epr_socket.create_keep()[0]
        epr_qubit.H()
        result = epr_qubit.measure()
        yield from connection.flush()
        print(f"{ns.sim_time()} ns: Server measures local EPR qubit: {result}")

        
        #merchant side
        
        msocket = context.msockets[merchant]

       
        
        # get connection to quantum network processing unit
        connection = context.connection

        # Bob listens for messages on his classical socket
        message = yield from msocket.recv()
        print(f"{ns.sim_time()} ns: Client: {self.name} receives message: {message}")

        return {}
