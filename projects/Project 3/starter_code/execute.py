from qiskit import Aer
from qiskit.providers.aer import AerSimulator
from qiskit import execute
from qiskit.providers.aer.noise import *
from qiskit.circuit import *
from typing import Dict

def run_sim(qc: QuantumCircuit, num_shots: int) -> Dict[str, int]: 
    # If you want, you can adjust NoiseModel() to insert random errors automatically
    # However, since we are only implementing a subset of fault-tolerant procedures
    # (e.g. ancilla bits may not be initialized properly), we may observe that
    # not all single bit errors are always corrected
    sim = AerSimulator(noise_model=NoiseModel())
    result = execute(qc, backend=sim, shots=num_shots, optimization_level=0).result()
    return result.get_counts()