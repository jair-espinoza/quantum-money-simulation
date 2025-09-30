import secrets
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Constant QuBit Bases
BASIS_Z = "Z"
BASIS_X = "X"

simulator = AerSimulator()

# Generate a random bit & random bases in the X or Z direction
def rand_bit():
    return secrets.randbits(1)

def rand_bas():
    return BASIS_X if rand_bit() else BASIS_Z

# Generate a qubit in specfic bits and bases
def generate_qubit(basis, bit):
    qc = QuantumCircuit(1,1)

    # on Z-basis apply x gate to flip to |1>
    if basis == BASIS_Z:
        if bit == 1:
            qc.x(0)
    # on X-basis flip and apply Hadmard to |->
    else:
        if bit == 1:
            qc.x(0)
        qc.h(0)
    return qc

# Measue Qubit basis
def measure_bas(qc, basis):
    meas = qc.copy()

    # on X-basis roate to measure
    if basis == BASIS_X:
        meas.h(0)

    meas.measure(0,0)
    job = simulator.run(meas, shots=1)
    result = job.result().get_counts()
    key = list(result.keys())[0]
    return int(key)