# Quantum-digital-payment


# Steps
1. Client initiate payment protocol with Bank.
2. Bank generates classical information for client token C.
3. Bank generates n bits of 0/1 as key(b) and basis(B).
4. Bank generates n |0> qubit list. 
5. Bank applies X gate to the ith qubit whenever the ith bit of b is 1. Then it applies H gate whenever the ith bit of B is 1. Now we have a qubit list called P. P is the payment token.
6. Bank send P and C to the Client. 

7. Client compute m=MAC(C,MerchantID). Where MAC(Message Authentication Code) function is the encyption function using a hash function, C and MerchantID.
8. Client measures list P by 


