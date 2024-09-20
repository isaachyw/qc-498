from qiskit import QuantumCircuit

from qiskit.circuit import QuantumRegister, ClassicalRegister, AncillaRegister
from qiskit.circuit.library.standard_gates import SXGate, MCXGate

from typing import List

# RESTRICTIONS ON CNF (you do not need to verify these):
# every variable appears at least once in CNF
# no variable appears twice in one term
# variable IDs always appear in ascending order (ignoring minus signs)
# names appear in the same relative order for each term
# (see spec for examples of invalid CNFs)


def bf_to_phase_oracle(bf_oracle: QuantumCircuit, num_vars: int) -> QuantumCircuit:
    """Returns a QuantumCircuit that flips the phase if f(x)=1
    Args:
        bf_oracle: Bitflip oracle to be converted to a phase oracle
        num_vars: How many variables are taken as input to the oracle"""
    pass

def get_bitflip_oracle(cnf: List[List[int]], num_vars: int) -> QuantumCircuit:
    """Returns a QuantumCircuit that flips qubit[num_var] if f(x) = 1
    Args:
        cnf: Non-empty array of clauses of literals
        num_vars: How many variables are taken as input to the oracle"""
    pass