from typing import List
import string
import secrets
import netsquid as ns
from netqasm.sdk.classical_communication.socket import Socket
from netqasm.sdk.connection import BaseNetQASMConnection
from netqasm.sdk.epr_socket import EPRSocket

from squidasm.sim.stack.program import Program, ProgramContext, ProgramMeta

class BankPrograme(Program):
    def __init__(self, client_name: str, merchants: List[str], lambda_parameter, C):
        self.client = client_name
        self.merchants = merchants
        self.parties = [client_name] + merchants
        self.lambda_parameter = lambda_parameter

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="sqdp_program",
            csockets=self.parties,
            epr_sockets=self.client,
            max_qubits=self.lambda_parameter,
        )

    def generate_random_string(lenght = 256):
        letters = string.ascii_letters + string.digits
        random_string = ''.join(secrets.choice(letters) for i in range(lenght))
        return random_string

    def run(self, context: ProgramContext):
        connection: BaseNetQASMConnection = context.connection

        #client side
        
        # get classical socket to peer
        csocket: Socket = context.csockets[self.parties[0]]
        epr_socket: EPRSocket = context.epr_sockets[self.client]

        # send a string message via a classical channel
        # generate C and fi
        #C = generate_random_string(256)
        #csocket.send(C)
        #print(f"{ns.sim_time()} ns: Server sends message: {C}")

        # Register a request to create an EPR pair, then apply a Hadamard gate on the epr qubit and measure
        # lambda = 128
        B = np.random.randint(0, 2, lambda_parameter)

        # for i in range(lambda):
        #    epr_socket.create_keep(i)[]

        epr_qubit = epr_socket.create_keep(lambda_parameter)

        for i in range(lambda_parameter):
            if B[i] == 1:
                epr_qubit[i].H()        
            b[i] = epr_qubit.measure()
        yield from connection.flush()
        print(f"{ns.sim_time()} ns: Server measures local EPR qubit: {result}")

        
        #merchant side
        # msocket_list = []
        # for merchant in self.merchants:
        #    msocket = context.msockets[merchant]
        #    msocket_list.append(msocket)

        #one merchant
        msocket = context.csockets[self.parties[1]]
        message = yield from msocket.recv()
        #split by space
        information = message.split()
        K_str = information[1]
        client_id = information[0]
        merchant_id = information[2]

        #merchant_id 

        # Calculate the MAC(C, M)
        poly1305 = Poly1305(C)
        m = poly1305.update(base64.b64decode(merchant_id))
        m = m.finalize()

        # Authenticaation
        verified = True
        m_list = list(m)
        k_list = []
        for elem in K_str:
            k_list.append(int(elem))
        j = 0
        for m_byte in m_list:
            i = 0
            while (i < 8):
                bit = (m_byte >> i) & 1
                if (bit == B[j]):
                    if k_list[j] != b[j]:
                        verified = False
                        break
                j += 1
                i += 1
        
        if verified:
            print(f"{ns.sim_time()} ns: Bank verifies the transaction with merchant {merchant_id} and client {client_id}")
        else:
            print(f"{ns.sim_time()} ns: Bank rejects the transaction with merchant {merchant_id} and client {client_id}")
        
        # get connection to quantum network processing unit
        connection = context.connection

        # Bob listens for messages on his classical socket
        message = yield from msocket.recv()
        print(f"{ns.sim_time()} ns: Client: {self.name} receives message: {message}")

        return {}
