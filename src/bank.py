from .qBits import rand_bas, rand_bit, generate_qubit, measure_bas
import secrets

"""
Bank Will Be Responsible For
    - Creating Bills
    - Keeping Bases  
    - Verifying Bills
"""

class Bank:

    # notes stored 
    def __init__(self, n_qubits):
        self.notes = {}
        self.n_qubits = n_qubits

    # mint a quantum bill
    def mint(self):
        bases = [rand_bas() for _ in range(self.n_qubits)]
        bits = [rand_bit() for _ in range(self.n_qubits)]
        note = [generate_qubit(b,x) for b,x in zip(bases, bits)]
        serial = secrets.token_hex(8)
        self.notes[serial] = (bases, bits)
        return serial, note
    
    def verify(self, serial, note):
        if serial not in self.notes:
            return False  # serial unknown

        bases, bits  = self.notes[serial]

        if len(note) != len(bases):
            return False

        for qc, b, x in zip(note, bases, bits):
            if measure_bas(qc, b) != x:
                return False
        return True