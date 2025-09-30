from src.bank import Bank
from src.qAgent import Agent

def test_qagent():
    N_QUBITS = 10
    N_TRAILS = 10

    # Init Bank & qAgent
    bank = Bank(n_qubits=N_QUBITS)
    agent = Agent(bank=bank)

    for _ in range(N_TRAILS):
        agent.withdraw()
    
        # Verify Working Wallet and Withdrawl
        print("Agent's Wallet After Withdrawing")
        print(agent.wallet, "\n")

        agent.deposit()
        
        # Verify Working deposite
        print("Agent's Wallet After Despoiting")
        print(agent.wallet, "\n")

test_qagent()