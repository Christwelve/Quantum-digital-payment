# Quantum-digital-payment

Team: Md Shadnan Azwad Khan, Chin-Te LIAO, Christina Repou, Anne Marin,
Flavia Voicu, Christian Meng, Sacha Ulysse Jeoffret

## Introduction
This project presents a simulation of a quantum-digital payment protocol as described in the paper "Demonstration of quantum-digital payments" (Nature Communications, 14(1), June 2023). It utilizes SquidASM from the NetSquid Simulator to model the interactions between a Client, a Merchant, and a Bank/Credit Card Institute (Trusted Third Party, TTP) in a secure quantum payment environment.

## Objective
The main objective is to simulate the execution of the quantum-digital payment protocol, ensuring secure transactions even in the presence of untrusted quantum and classical communication channels. The application also explores scenarios involving malicious behaviors to test the robustness of the protocol.

## Protocol Overview
1. **Quantum State Preparation**: The TTP generates a random bitstring and a conjugate basis-string, encoding them onto a quantum state sent to the Client.  
2. **MAC Calculation**: The Client calculates a Message Authentication Code (MAC) using a secret token and the Merchant's identifier, measuring the received quantum state accordingly.  
3. **Transaction Initiation**: The Client sends its public identifier and the measurement result to the Merchant, who forwards it to the TTP.
4. **Transaction Verification**: The TTP verifies the transaction based on the MAC and the measurement result, authorizing the purchase if the validation is successful.  

## Steps
1. Client initiates payment protocol with Bank.
2. Bank generates classical information for client token $C$.
3. Bank generates $n$ bits of 0/1 as key ($b$) and basis ($B$).
4. Bank generates $n|0>$ qubit list. 
5. Bank applies $X$ gate to the $i^{th}$ qubit whenever the ith bit of $b$ is 1. Then it applies $H$ gate whenever the $i^{th}$ bit of $B$ is 1. Now we have a qubit list called $P$. $P$ is the payment token.
6. Bank sends $P$ using quantum communication and $C$ classically to the Client.

7. Client computes $m = MAC(C, MerchantID)$. Where the MAC (Message Authentication Code) function is the encyption function using a hash function, $C$ and $MerchantID$.
8. Client measures list $P$ using $m$ as a basis string. The result of the measurement is the cryptogram $K$.
9. Client sends $ClientID$ and $K$ to the Merchant.

10. Merchant takes the $ClientID$ and $K$ and sends both along with $MerchantID$ to the Bank.
  
11. Bank looks up the $C$, $b$, and $B$ corresponding to the $ClientID$ it recieved from the Merchant.
12. Bank computes $m = MAC(C, MerchantID)$.
13. Bank compares every $i^{th}$ bit of $m$ and the previously generated $B$, if $m_i = B_i$ then it compares the $i^{th}$ bit of $K$ and $b$, to check if $K_i = b_i$. If both checks pass, the transaction is accepted, otherwise it is rejected.



## Technologies
- **Quantum Simulation**: SquidASM (NetSquid Simulator) version b0.0.5
- **Programming Language**: Python3.10
- **Supported Qubit Technologies**: Generic hardware, NV centers, color centers (as available in SquidASM)

## Pre-requisites
- **Python Version**: Python >3 is necessary.
- **NetSquid Forum Account**: Create an account on the [NetSquid forum](https://forum.netsquid.org/) and use your credentials in SquidASM installation.
- **SquidASM Installation**: Follow the SquidASM tutorial for installation [here](https://squidasm.readthedocs.io/en/latest/installation.html).
SquidASM only works on Linux and MacOS. For Windows users we recommend using [WSL](https://learn.microsoft.com/en-us/windows/wsl/install).

## Environment Installation
```bash
# Clone the repository
git clone https://github.com/Christwelve/Quantum-digital-payment.git

# Navigate to the project directory
cd Quantum-digital-payment/

# Install Python (if not installed)
sudo apt update
sudo apt install python3

# Install dependencies
pip install numpy==1.19.5

# Follow SquidASM installation instructions as per the provided link
```

## Usage
To run the simulation:
```bash
python3 run_SecureQuantumDigitalPayments.py
```

## Simulation Scenarios
- **Honest Client and Merchant**: Simulate the protocol execution with both parties behaving honestly.
- **Malicious Merchant**: Demonstrate the impact of a forged output tag.
- **Malicious Client**: Explore the effects of exploiting device imperfections for double-spending.

## Results
- **Quantum State Fidelity** : The fidelity of quantum states is crucial for the security and effectiveness of the payment protocol. We can varied the physical parameters of qubits and quantum links to observe their impacts. Also, it seems SquidASM only support < 100qbits simulations.

- **Simulation of Malicious Behaviors by Test Scenarios** :  
*Malicious Merchant*: The simulator was able to detect and reject of fraudulent transaction attempts where a malicious merchant tried to forge the output tag.  
*Malicious Client*: The protocol was resilient against double-spending attempts. The strategy of measuring on different bases to create two valid tokens was effectively countered by the TTP's verification mechanism.  

- **Implications and Recommendations**:  
*Optimization of Physical Parameters*: The results underscore the importance of optimizing the physical parameters of qubits and communication channels to maximize the fidelity of quantum states.  
*Security Against Attacks*: To further bolster the security of the quantum digital payment protocol, we explored the integration of Quantum Key Distribution (QKD) algorithms for secure communication channels (not implemented).  

## Contributions
This project was developed as part of the [Pan-European Quantum Internet Hackathon 2024](https://quantuminternetalliance.org/quantum-internet-hackathon-2024/). The event took place on February 15th and 16th, and this application is the result of one of our team's work these two days at LIP6 laboratory, Sorbonne Université, Paris.

Your contributions can help us improve the functionality, security, and efficiency of this quantum digital payment system. Whether it's through code contributions, bug reports, feature requests, or documentation, every bit of help is greatly appreciated.

## References
- Peter Schiansky, et al. "Demonstration of quantum-digital payments." Nature Communications, 14(1), Jun 2023.

## Contact
We welcome contributions and suggestions to improve this project. If you are interested in contributing, please contact [@Chriswelve](https://github.com/Chriswelve) on GitHub for more information on how to get involved.

## Contributors
https://github.com/LiaoChinTe
https://github.com/shadwad
https://github.com/Christwelve
https://github.com/dendeaisd
https://github.com/SachaUlysse
https://github.com/ChrRepou
https://github.com/AMarin-git
