import unittest
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator
from qiskit_aer import AerSimulator
from p1 import LQ3K

test_gate = 2


class TestP1Public(unittest.TestCase):
    @unittest.skipIf(test_gate != 1, "skip if not one qubit gate")
    def test_simple_x(self):
        test = LQ3K(1)
        test.x(0)
        self.assertTrue(np.array_equal(test.get_unitary(), [[0, 1], [1, 0]]))
        self.assertTrue(np.array_equal(test.evolve([1, 0]), [0, 1]))
        self.assertEqual(test.simulate_run([1, 0]), 1)

    @unittest.skipIf(test_gate != 1, "skip if not one qubit gate")
    def test_simple_y(self):
        init_state: np.ndarray = np.array([1, 0])
        qc = QuantumCircuit(1)
        qc.initialize(init_state, 0)
        lc = LQ3K(1)
        qc.y(0)
        lc.y(0)
        self.assertTrue(np.array_equal(lc.evolve(init_state), Statevector(qc).data))

    @unittest.skipIf(test_gate != 2, "skip if not two qubit gate")
    def test_simple_swap(self):
        for i in range(2**2):
            init_state: np.ndarray = np.array([0] * 2**2)
            init_state[i] = 1
            operator_circuit = QuantumCircuit(2)
            operator_circuit.cx(1, 0)
            circuitOp = Operator.from_circuit(operator_circuit)
            print(circuitOp.data)
            qc = QuantumCircuit(2)
            qc.initialize(init_state, qc.qubits)
            lc = LQ3K(2)
            qc.compose(operator_circuit, inplace=True)
            lc.cx(0, 1)
            lc_state = lc.evolve(init_state)
            qc_state = Statevector(qc).data
            self.assertTrue(np.array_equal(lc_state, qc_state))


if __name__ == "__main__":
    unittest.main()
