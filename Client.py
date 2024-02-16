from typing import List

import netsquid as ns
from netqasm.sdk.classical_communication.socket import Socket
from netqasm.sdk.connection import BaseNetQASMConnection
from netqasm.sdk.epr_socket import EPRSocket

from squidasm.sim.stack.program import Program, ProgramContext, ProgramMeta

import random

import base64

from cryptography.hazmat.primitives import poly1305
from cryptography.hazmat.backends import default_backend

class ClientProgram(Program):
	def __init__(self, parties: List[str], lambda_parameter, C, M: List[str], client_name: str):
		self.parties = parties
		self.lambda_parameter = lambda_parameter
		self.C = C
		self.M = M
		self.client_name = client_name

	@property
	def meta(self) -> ProgramMeta:
		return ProgramMeta(
			name="sqdp",
			csockets=self.parties,
			epr_sockets=self.parties,
			max_qubits=self.lambda_parameter, #not sure maybe should be one
		)

	def run(self, context: ProgramContext):
		connection: BaseNetQASMConnection = context.connection

		# classical connection with ttp
		csocket_ttp: Socket  = context.csockets[self.parties[0]]

		# connect with ttp for qubit exchange
		epr_socket: EPRSocket = context.epr_sockets[self.parties[0]]

		# Receiving the |P> from ttp
		epr_qubits = []
		for i in range(self.lambda_parameter):
			epr_qubits.append(epr_socket.recv_keep()[0])

		# Select a merchant randomly
		#merchant_id = random.randint(1, len(parties))
		merchant_id = 0
		print(f'Merchant id: {merchant_id}')

		# Connect with merchant
		csocket_merchant: Socket  = context.csockets[self.parties[merchant_id + 1]]

		# Calculate the MAC(C, M)
		p = poly1305.Poly1305(self.C)
		p.update(base64.b64decode(self.M[merchant_id - 1]))
		m = p.finalize()

		# Calculate the K
		K = []
		m_list = list(m)
		#qubit_list = list(epr_qubits)
		j = 0
		for m_byte in m_list:
			i = 0
			while (i < 8):
				bit = (m_byte >> i) & 1
				qubit = epr_qubits[j]
				if (bit == 1):
					qubit.H()
				K.append(qubit.measure())
				j += 1
				i += 1
			if (j > 8 * (self.lambda_parameter // 8) - 1):
				break
		yield from connection.flush()
		# Send K,C back to merchant
		# csocket_merchant.send(self.client_name)
		K_list = []
		for elem in K:
			K_list.append(str(elem))
		K_str = ''.join(K_list)
		final = self.client_name + " " + K_str
		csocket_merchant.send(final)
		print(f"{ns.sim_time()} ns: Client sends to Merchant: {K_str}")


		return {}
