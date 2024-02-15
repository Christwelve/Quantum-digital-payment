from typing import List

import netsquid as ns
from netqasm.sdk.classical_communication.socket import Socket
from netqasm.sdk.connection import BaseNetQASMConnection
from netqasm.sdk.epr_socket import EPRSocket

from squidasm.sim.stack.program import Program, ProgramContext, ProgramMeta

import random

import base64

from cryptography.hazmat.primitives.poly1305 import Poly1305
from cryptography.hazmat.backends import default_backend
# from os import urandom

class Client(Program):
	def __init__(self, parties: List[str], lamda, C, M: List[str]):
		self.parties = parties
		self.lamda = lamda
		self.C = C
		self.M = M

	@property
	def meta(self) -> ProgramMeta:
		return ProgramMeta(
			name="client_program",
			csockets=self.parties,
			epr_sockets=self.parties,
			max_qubits=self.lamda, #not sure maybe should be one
		)

	def run(self, context: ProgramContext):
		connection: BaseNetQASMConnection = context.connection

		# classical connection with ttp
		csocket_ttp: Socket  = context.csockets[0]

		# connect with ttp for qubit exchange
		epr_socket: EPRSocket = context.epr_sockets[0]

		# Receiving the |P> from ttp
		epr_qubits = epr_socket.recv_keep(number=lamda)

		# Select a merchant randomly
		merchant_id = random.randint(1, len(parties))
		print(f'Merchant id: {merchant_id}')

		# Connect with merchant
		csocket_merchant: Socket  = context.csockets[merchant_id]

		# Calculate the MAC(C, M)
		poly1305 = Poly1305(C)
		m = poly1305.update(base64.b64decode(M[merchant_id - 1]))
		m = m.finalize()

		# Calculate the K
		K = []
		m_list = list(m)
		qubit_list = list(epr_qubits)
		j = 0
		for m_byte in m_list:
			i = 0
			while (i < 8):
				bit = (m_byte >> i) & 1
				qubit = qubit_list[j]
				if (bit == 1):
					qubit.H()
				K[j] = qubit.measure()
				j += 1
				i += 1
		yield from connection.flush()

		# Send K,C back to merchant
		csocket_merchant.send(self.name)
		K_str = ''.join(K)
		csocket_merchant.send(K_str)
		print(f"{ns.sim_time()} ns: Client sends to Merchant: {K_str}")


		return {}
