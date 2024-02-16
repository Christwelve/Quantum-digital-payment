# Quantum-digital-payment


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
  
11. Bank finds the $C$, $b$, and $B$ corresponding to the $ClientID$ it recieved from the merchant
12. Bank computes $m = MAC(C, MerchantID)$.
13. Bank compares every $i^{th}$ bit of $m$ and the previously generated $B$, if $m_i = B_i$ then it compares the $i^{th}$ bit of $K$ and $b$, to check if $K_i = b_i$. If both checks pass, the transaction is accepted, otherwise it is rejected.
