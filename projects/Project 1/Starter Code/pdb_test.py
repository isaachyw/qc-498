import numpy as np

# Import Qiskit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer, AerSimulator
from qiskit.quantum_info import Operator

qc = QuantumCircuit(2)
qc.swap(0, 1)
op = Operator.from_circuit(qc)
print(op.data)
