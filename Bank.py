from typing import List

import netsquid as ns
from netqasm.sdk.classical_communication.socket import Socket
from netqasm.sdk.connection import BaseNetQASMConnection
from netqasm.sdk.epr_socket import EPRSocket

from squidasm.sim.stack.program import Program, ProgramContext, ProgramMeta


class ClientPrograme(Program):
    def __init__(self, name: str, server_name: str):
        self.name = name
        self.server_name = server_name

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="tutorial_program",
            csockets=[self.server_name],
            epr_sockets=[self.server_name],
            max_qubits=1,
        )

    def run(self, context: ProgramContext):
        # get classical socket to peer
        csocket = context.csockets[self.server_name]
        # get EPR socket to peer
        epr_socket = context.epr_sockets[self.server_name]
        # get connection to quantum network processing unit
        connection = context.connection

        # Bob listens for messages on his classical socket
        message = yield from csocket.recv()
        print(f"{ns.sim_time()} ns: Client: {self.name} receives message: {message}")

        # Listen for request to create EPR pair, apply a Hadamard gate on the epr qubit and measure
        epr_qubit = epr_socket.recv_keep()[0]
        epr_qubit.H()
        result = epr_qubit.measure()
        yield from connection.flush()
        print(
            f"{ns.sim_time()} ns: Client: {self.name} measures local EPR qubit: {result}"
        )

        return {}