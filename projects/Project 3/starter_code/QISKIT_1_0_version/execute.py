from qiskit import *
from qiskit import transpile
from qiskit_aer import AerSimulator
from typing import Dict

from qiskit_aer.noise import *
    
def run_sim(qc: QuantumCircuit, num_shots: int) -> Dict[str, int]:
    # If you want, you can adjust NoiseModel() to insert random errors automatically
    # However, since we are only implementing a subset of fault-tolerant procedures
    # (e.g. ancilla bits may not be initialized properly), we may observe that
    # not all single bit errors are always corrected
    sim = AerSimulator(noise_model=NoiseModel())
    transpiled = transpile(qc, sim)
    result = sim.run(transpiled, shots=num_shots).result()
    return result.get_counts(transpiled)
