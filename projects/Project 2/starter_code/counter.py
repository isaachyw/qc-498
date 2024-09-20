from qiskit import *
import numpy as np
import math
from typing import List, Tuple

import grover


def qft(n: int) -> QuantumCircuit:
    """Returns a QuantumCircuit implementing the Quantum Fourier Transform
    for n bits
    Args:
        n: Width of the quantum circuit"""
    pass


def quantum_counter(cnf: List[List[int]], num_vars: int, precision: int) -> QuantumCircuit:
    """Returns quantum circuit implementing quantum counter algorithm,
    which estimates the number of solutions to a given CNF function"
    four quantum counting result 
    Args:
        cnf: Array of clauses of literals
        num_vars: number of variables using in quantum counting algorithm
        precision: number of counting bits using in quantum counting"""
    pass