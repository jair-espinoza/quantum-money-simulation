from src.bank import Bank
from src.regularAttacker import RegularAttacker

def test_regular_attacker():
    N_QUBITS = 10
    N_TRIALS = 5

    bank = Bank(n_qubits=N_QUBITS)
    attacker = RegularAttacker(bank=bank)

    for i in range(N_TRIALS):
        print(f"\n=== Trial {i+1} ===")

        # Withdraw
        serial, note = attacker.withdraw()
        print("Withdrawn note:", {serial: note})

        # Forge
        serial, forged_note = attacker.forge(serial)
        print("Forged note:", {serial: forged_note})

        # Deposit
        serial, success = attacker.deposit()

    # Final states
    print("\nFinal attacker wallet (real notes left):", attacker.wallet)
    print("\nFinal failed forged notes:", attacker.failed_notes)
    print("\nSuccessfully replicated bills:", attacker.passed_notes)
    
test_regular_attacker()
