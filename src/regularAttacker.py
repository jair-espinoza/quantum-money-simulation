from .qBits import rand_bas, measure_bas, generate_qubit

class RegularAttacker:

    def __init__(self, bank):
        self.bank = bank
        self.forged_notes = {}
        self.wallet = {}
        self.failed_notes={}
        self.passed_notes={}

    def withdraw(self):
        serial, note = self.bank.mint()
        self.wallet[serial] = note
        return serial, note
    
    def forge(self, serial):
        if serial not in self.wallet:
            raise ValueError("Get A Real Note First")
        
        note  = self.wallet[serial]
        guessed_note = []
        
        # Using the same serial number try to replicate the bills basis
        for qc in note:
            basis_guess = rand_bas()
            bit_guess = measure_bas(qc, basis_guess)
            guessed_note.append(generate_qubit(basis_guess, bit_guess))

        # Store Fake Note
        self.forged_notes[serial] = guessed_note
        return serial, guessed_note

    def deposit(self):

        # Try to deposit a forged note first
        if self.forged_notes:
            serial, forged_note = self.forged_notes.popitem()
            success = self.bank.verify(serial, forged_note)
            print(f"Deposit {'SUCCESS' if success else 'FAILURE'} for forged Note serial {serial}")

            if not success:
                self.failed_notes[serial] = forged_note

                # Hand Over Real note To Avoid Suspicion
                if serial in self.wallet:
                    real_note = self.wallet.pop(serial)
                    self.bank.verify(serial, real_note)
                    print(f"Real note deposited to avoid suspicion")

            # the bill replicated was successful         
            else: 
                self.passed_notes[serial] = forged_note
            return serial, success

        raise ValueError("No bill to deposit")
