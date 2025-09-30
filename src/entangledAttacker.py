from .qBits import rand_bas, measure_bas, generate_qubit
from .bank import Bank
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


simulator = AerSimulator()

class EntangledAttacker:
    def __init__(self, bank, threshold=int):
        self.bank = bank
        self.threshold = threshold
        self.wallet = {}           
        self.best_serial = None   
        self.best_conf = 0.0
        self.memory = {}           
        self.forged_notes = {}

    def withdraw(self):
        serial, note = self.bank.mint()
        self.wallet[serial] = note
        return serial, note

    def probe_qubit(self, qc, true_basis):
        probe_basis = rand_bas()
        bit_guess = measure_bas(qc, probe_basis)

        confidence = 0.95 if probe_basis == true_basis else 0.55
        return bit_guess, probe_basis, confidence

    def probe_bill(self, serial):

        note = self.wallet[serial]
        bases, bits = self.bank.notes[serial]
        total_conf = 0
        local_memory = {}

        for i, (qc, true_basis) in enumerate(zip(note, bases)):
            bit_guess, probe_basis, confidence = self.probe_qubit(qc, true_basis)
            local_memory[i] = (probe_basis, bit_guess, confidence)
            total_conf += confidence

        avg_conf = total_conf / len(note)
        return avg_conf, local_memory

    def evaluate(self, serial):
        avg_conf, local_memory = self.probe_bill(serial)

        if avg_conf >= self.threshold and avg_conf > self.best_conf:
            # Replace current best bill
            if self.best_serial:
                # return old best bill safely
                old_note = self.wallet.pop(self.best_serial)
                self.bank.verify(self.best_serial, old_note)

            self.best_serial = serial
            self.best_conf = avg_conf
            self.memory = local_memory
            print(f"New best bill {serial} with confidence {avg_conf:.2f}")
            return True
        else:
            # Not good enough, return it to bank
            real_note = self.wallet.pop(serial)
            self.bank.verify(serial, real_note)
            print(f"Bill {serial} discarded with confidence {avg_conf:.2f}")
            return False

    def forge_best(self):

        serial = self.best_serial
        note = self.wallet[serial]
        forged_note = []

        for i in range(len(note)):
            basis, bit, conf = self.memory.get(i, (rand_bas(), 0, 0.5))
            if conf < 0.8:  # not confident → guess
                basis = rand_bas()
                bit = 0
            forged_note.append(generate_qubit(basis, bit))

        self.forged_notes[serial] = forged_note
        return serial, forged_note

    def deposit_best(self):

        serial, forged_note = self.forge_best()
        success = self.bank.verify(serial, forged_note)
        print(f"Forged deposit for {serial} {'SUCCESS' if success else 'FAILURE'} "
              f"(confidence {self.best_conf:.2f})")
        return serial, success
    
    