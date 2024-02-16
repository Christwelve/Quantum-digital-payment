# Quantum-digital-payment

## Introduction
This project presents a simulation of a quantum-digital payment protocol as described in the paper "Demonstration of quantum-digital payments" (Nature Communications, 14(1), June 2023). It utilizes SquidASM from the NetSquid Simulator to model the interactions between a Client, a Merchant, and a Bank/Credit Card Institute (Trusted Third Party, TTP) in a secure quantum payment environment.

## Objective
The main objective is to simulate the execution of the quantum-digital payment protocol, ensuring secure transactions even in the presence of untrusted quantum and classical communication channels. The application also explores scenarios involving malicious behaviors to test the robustness of the protocol.

## Protocol Overview
1. **Quantum State Preparation**: The TTP generates a random bitstring and a conjugate basis-string, encoding them onto a quantum state sent to the Client.
2. **MAC Calculation**: The Client calculates a Message Authentication Code (MAC) using a secret token and the Merchant's identifier, measuring the received quantum state accordingly.
3. **Transaction Initiation**: The Client sends its public identifier and the measurement result to the Merchant, who forwards it to the TTP.
4. **Transaction Verification**: The TTP verifies the transaction based on the MAC and the measurement result, authorizing the purchase if the validation is successful.

# Steps
1. Client initiates payment protocol with Bank.
2. Bank generates classical information for client token $C$.
3. Bank generates $n$ bits of 0/1 as key ($b$) and basis ($B$).
4. Bank generates $n|0>$ qubit list. 
5. Bank applies $X$ gate to the ith qubit whenever the ith bit of $b$ is 1. Then it applies $H$ gate whenever the $i^{th}$ bit of $B$ is 1. Now we have a qubit list called $P$. $P$ is the payment token.
6. Bank sends $P$ using quantum communication and $C$ classically to the Client.

7. Client computes $m = MAC(C, MerchantID)$. Where the MAC (Message Authentication Code) function is the encyption function using a hash function, $C$ and $MerchantID$.
8. Client measures list $P$ using $m$ as a basis string. The result of the measurement is the cryptogram $K$.
9. Client sends $ClientID$ and $K$ to the Merchant.

10. Merchant takes the $ClientID$ and $K$ and sends both along with $MerchantID$ to the Bank.
  
11. Bank looks up the $C$, $b$, and $B$ corresponding to the $ClientID$ it recieved from the Merchant.
12. Bank computes $m = MAC(C, MerchantID)$.
13. Bank compares every $i^{th}$ bit of $m$ and the previously generated $B$, if $m_i = B_i$ then it compares the $i^{th}$ bit of $K$ and $b$, to check if $K_i = b_i$. If both checks pass, the transaction is accepted, otherwise it is rejected.



## Technologies
- **Quantum Simulation**: SquidASM (NetSquid Simulator)
- **Programming Language**: Python
- **Supported Qubit Technologies**: Generic hardware, NV centers, color centers (as available in SquidASM)

## Pre-requisites
- **Python Version**: Python >3 is necessary.
- **NetSquid Forum Account**: Create an account on the [NetSquid forum](https://forum.netsquid.org/) and use your credentials in SquidASM installation.
- **SquidASM Installation**: Follow the SquidASM tutorial for installation [here](https://squidasm.readthedocs.io/en/latest/installation.html).
SquidASM only works on Linux and MacOS. For Windows users we recommend using [WSL](https://learn.microsoft.com/en-us/windows/wsl/install).

