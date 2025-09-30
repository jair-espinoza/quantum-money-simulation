from src.bank import Bank
from src.entangledAttacker import EntangledAttacker

class test_en_attacker():
    N_QUBITS = 10
    N_TRAILS = 10
    THRESHOLD = .80

    bank = Bank(N_TRAILS)
    attacker = EntangledAttacker(bank=bank, threshold=THRESHOLD)

    for i in range(N_TRAILS):
        print(f"\n=== Trial {i+1} ===")

        serial, note = attacker.withdraw()
        print("Withdrawn note:", {serial: note})

        # eval to note to keep
        kept = attacker.evaluate(serial)
        status = "KEPT" if kept else "Discarded"
        print(f"Serial: {serial} was {status}")

        # current best note
        best = attacker.best_serial or "None"
        print(f"Current Best is {best} | avg_conf={attacker.best_conf:2f}")

        # if we have a good note try to forge it
        if attacker.best_serial:
            serial, forged_note = attacker.forge_best()
            forged_serial, success = attacker.deposit_best()
            result = "SUCCESS" if success else "Failed"
            print(f"Forged deposit on Note {forged_serial}: {result}")

        if attacker.best_serial:
            print(f"Our Best Final Note Was: {attacker.best_serial}")
        else:
            print({"No Good Note To Forge"})
    
test_en_attacker()