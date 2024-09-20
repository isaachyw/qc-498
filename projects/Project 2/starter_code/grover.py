from qiskit import *
from typing import List

import oracle

def diffuser(num_vars: int) -> QuantumCircuit:
    """Returns QuantumCircuit that rotates the state around |s>
    Args:
        num_vars: How many variables are input into the diffuser"""
    pass

def grover_iteration(cnf: List[List[int]], num_vars: int) -> QuantumCircuit:
    """Returns a QuantumCircuit implementing a single Grover iteration
    (i.e. phase oracle of provided cnf + diffuser)
    Args:
        cnf: Array of clauses of literals
        num_vars: How many variables are taken as input to the oracle"""
    pass

def grover(cnf: List[List[int]], num_vars: int, num_iters: int) -> QuantumCircuit:
    """Returns a QuantumCircuit implementing a full Grover implementation
    with specified number of iterations
    Args:
        cnf: Array of clauses of literals
        num_vars: How many variables are taken as input to the oracle
        num_iters: How many Grover iterations should be included"""
    pass