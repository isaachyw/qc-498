from operator import length_hint
import unittest

import sys

from qiskit import *
from qiskit.circuit import *
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector

from qiskit import transpile

import numpy as np
import math

import driver, oracle, grover, counter

# adds classical bits to circuit which is result
# of measuring select qubits
def measure_qubits(circ, indices):
    circ_m = QuantumCircuit(circ.num_qubits, circ.num_clbits)

    num_qubits = len(indices)
    cr = ClassicalRegister(num_qubits)
    circ.add_register(cr)
    circ.measure(indices,range(num_qubits))

    return circ

# for a given device-under-test (DUT), initialize circuit with provided input,
# measure each of the specified qubits, and simulate num_shots runs, returning
# results
def test_circuit(dut, input_val, measure_indices, num_shots):
    circ = QuantumCircuit(dut.num_qubits, dut.num_clbits)
    initial_state = Statevector.from_int(input_val,2**circ.num_qubits)
    circ.set_statevector(initial_state)
    circ.compose(dut, inplace=True)
    measure_qubits(circ, measure_indices)

    sim = AerSimulator()
    new_circuit = transpile(circ, sim)
    result = sim.run(new_circuit, shots=num_shots).result()

    return result.get_counts(circ)

# for a given device-under-test (DUT), return unitary matrix
def get_circuit_unitary(dut):
    dut.save_unitary()
    sim = AerSimulator()
    new_circuit = transpile(dut, sim)
    result = sim.run(new_circuit, shots=1).result()
    mat = np.asarray(result.get_unitary(dut))
    
    return mat

class PublicTests(unittest.TestCase):

    def test_version(self):
        if sys.version_info >= (3,8):
            print("\nWarning: your Python version is ", sys.version)
            print("The autograder is currently limited to Python 3.7.5. Double check that your code will run correctly.")


    def test_simple_oracle(self):
        # (var1 or var2) and (~var1 or ~var2)
        # (solutions should be 01 and 10)
        input = [[1,2],[-1,-2]]
        num_vars = 2

        # create oracle
        circ = oracle.get_bitflip_oracle(input, num_vars)

        num_shots = 10

        # input 0b00 and verify output is 0
        counts = test_circuit(circ.copy(), 0, {num_vars}, num_shots)
        self.assertEqual(counts, {'0':num_shots})

         # input 0b01 and verify output is 1
        counts = test_circuit(circ.copy(), 1, {num_vars}, num_shots)
        self.assertEqual(counts, {'1':num_shots})
        
        # should be able to get unitary matrix (this test does not verify that it's correct)
        get_circuit_unitary(circ.copy())


    def test_simple_grover(self):
        # (var1) and (var2)
        # (solutions should be 11)
        input = [[1],[2]]
        num_vars = 2

        circ = grover.grover(input, num_vars, num_iters=1)

        num_shots = 10
        counts = test_circuit(circ.copy(), 0, range(num_vars), num_shots)
        self.assertEqual(counts, {'11': num_shots})
        
        # should be able to get unitary matrix (this test does not verify that it's correct)
        get_circuit_unitary(circ.copy())


    def test_simple_count(self):
        # 4 solutions, counter should return either 2 or 6
        input = [[1,-2],[2,3]]
        num_vars = 3
        precision = 3
        circ = counter.quantum_counter(input, num_vars, precision)

        num_shots = 1000
        counts = test_circuit(circ.copy(), 0, range(num_vars), num_shots)
        result = max(counts, key=counts.get)
        self.assertTrue(result == '010' or result == '110')
        
        # should be able to get unitary matrix (this test does not verify that it's correct)
        get_circuit_unitary(circ.copy())


    