from src.bank import Bank
from src.statisticalAttacker import StatAttacker

def test_stat_attacker():
    N_QUBITS = 10
    N_TRIALS = 5

    # init bank and attacker
    bank = Bank(n_qubits=N_QUBITS)
    attacker = StatAttacker(bank=bank)

    for i in range(N_TRIALS):
        print(f"\n=== Trial {i+1} ===")

        # Withdraw one bill
        serial, note = attacker.withdraw()
        print("Withdrawn note:", serial)

        # Attacker measures all qubits (collapsing the note)
        memory = attacker.measure_all(serial)
        print("Attacker memory:", memory)

        # Forge a note based on memory
        serial, forged_note = attacker.forge(serial)
        print("Forged note created for serial:", serial)

        # Deposit forged first, then real
        serial_deposit, success = attacker.deposit()
        if serial_deposit in attacker.failed_notes:
            print(f"Deposit FAILED for serial {serial_deposit} (moved to failed_notes)")
        else:
            print(f"Deposit {'SUCCESS' if success else 'FAILURE'} for serial {serial_deposit}")

    # Final state
    print("\nFinal attacker wallet:", attacker.forged_notes)
    print("Final failed forged notes:", attacker.failed_notes)

test_stat_attacker()