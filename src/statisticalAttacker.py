from .qBits import rand_bas, measure_bas, generate_qubit

class StatAttacker:
    def __init__(self, bank):
        self.bank = bank
        self.wallet = {}        
        self.memory = {}         
        self.forged_notes = {}
        self.failed_notes = {}

    def withdraw(self):
        serial, note = self.bank.mint()
        self.wallet[serial] = note
        return serial, note

    def measure_all(self, serial):
        if serial not in self.wallet:
            raise ValueError("No Bill in wallet.")

        note = self.wallet[serial]

        for i, qc in enumerate(note):
            basis_guess = rand_bas()
            bit_guess = measure_bas(qc, basis_guess)
            self.memory[i] = (basis_guess, bit_guess)
            
            # Collapse the state of the original note
            note[i] = generate_qubit(basis_guess, bit_guess)

        return self.memory

    def forge(self, serial):
        if serial not in self.wallet:
            raise ValueError("No Bill in wallet.")

        note = self.wallet[serial]
        forged_note = []
        for i in range(len(note)):
            basis, bit = self.memory.get(i, (rand_bas(), 0))
            forged_note.append(generate_qubit(basis, bit))

        self.forged_notes[serial] = forged_note
        return serial, forged_note

    def deposit(self):
        if self.forged_notes:
            serial, forged_note = self.forged_notes.popitem()
            success = self.bank.verify(serial, forged_note)
            print(f"Deposit {'SUCCESS' if success else 'FAILURE'} for forged note serial {serial}")

            if success:
                return serial, True

            # If forgery fails, try the real note
            if serial in self.wallet:
                real_note = self.wallet.pop(serial)
                real_success = self.bank.verify(serial, real_note)
                print(f"Real note deposit {'SUCCESS' if real_success else 'FAILURE'} ")

                if not real_success:
                    print(f"\nBoth Notes Failed")
                    self.failed_notes[serial] = real_note

                return serial, real_success 

        raise ValueError("No bill to deposit")
