import numpy as np
from sympy import matrix2numpy
import random


class LQ3K:
    """Create a new circuit with the specified number of qubits and no gates.

    Circuit supports limited measuring capabilities: all qubits are automatically measured
    at the end of the circuit when running "simulate_run"

    Args:
        num_qubits: total number of quantum bits in the circuit (can't be modified after
        initialization)

        Example:
            qc = LQ3K(2)
            qc.cx(0, 1)
            qc.get_unitary()

            # returns
            # [[1. 0. 0. 0.]
            # [0. 0. 0. 1.]
            # [0. 0. 1. 0.]
            # [0. 1. 0. 0.]]
            # note the endianness of bits: larger index is more significant
    """

    # contain a state vector and a unitary matrix

    class InvalidStateVector(Exception):
        """Not a valid state vector"""

    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.state_vector = np.zeros(2**num_qubits)
        self.unitary = np.identity(2**num_qubits)

    def evolve(self, initial_state):
        """Return the state vector after initial_state is passed through circuit

        Example:
            qc = LQ3K(1)
            qc.x(0)
            qc.evolve([1,0])

            [0. 1.]

        Returns: numpy.array representing state vector

        Raises:
            InvalidStateVector: When initial_state is not unit length."""
        # if initial_state is not unit length, raise InvalidStateVector
        if np.linalg.norm(initial_state) != 1:
            raise self.InvalidStateVector("Initial state is not unit length")
        return np.dot(self.unitary, initial_state)

    def __neighbour_swap(self, idx_1):
        print(f"neighbour swap {idx_1}")
        """apply SWAP gate to the qubit at idx_1 and idx_1+1"""
        assert idx_1 >= 0 and idx_1 < self.num_qubits - 1
        # Define the SWAP gate as a NumPy array
        swap_gate = np.array(
            [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype=complex
        )
        # expand it in to 2**self.num_qubits dimensions
        swap_gate_broadcast = np.kron(
            np.identity(2**idx_1),
            np.kron(swap_gate, np.identity(2 ** (self.num_qubits - idx_1 - 2))),
        )
        self.unitary = np.dot(swap_gate_broadcast, self.unitary)

    def swap(self, idx_1, idx_2):
        """Applies SWAP gate, switching the state of the two specified qubits
        A qubit CANNOT be swapped with itself"""
        smaller_idx = min(idx_1, idx_2)
        bigger_idx = max(idx_1, idx_2)
        # cumulatively apply neighbour swap (smaller_idx,smaller_idx+1), (smaller_idx+1,smaller_idx+2), ... (bigger_idx-1,bigger_idx)
        # and then go back from bigger_idx to smaller_idx
        for i in range(smaller_idx, bigger_idx):
            self.__neighbour_swap(i)
        for i in range(bigger_idx - 1, smaller_idx, -1):
            self.__neighbour_swap(i - 1)

    def ccx(self, control_qubit1, control_qubit2, target_qubit):
        """Applies CCX, also known as Toffoli gate, to the specified qubits"""
        pass

    def cx(self, control_qubit, target_qubit):
        """Applies CX, also known as controlled-NOT gate, to the specified qubits"""
        cx_gate = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
        # conditionally make swap make sure control_qubit is smaller than target_qubit
        if control_qubit > target_qubit:
            self.swap(control_qubit, target_qubit)
            control_qubit, target_qubit = target_qubit, control_qubit
        # if target qubit and control qubit are not ajacent, make them adjacent
        temp_target_qubit = target_qubit
        if target_qubit != control_qubit + 1:
            self.swap(control_qubit + 1, target_qubit)
        cx_gate_broadcast = np.kron(
            np.identity(2**control_qubit),
            np.kron(cx_gate, np.identity(2 ** (self.num_qubits - control_qubit - 2))),
        )
        self.unitary = np.dot(cx_gate_broadcast, self.unitary)
        # if target qubit and control qubit are not ajacent, swap back the target qubit
        self.swap(control_qubit + 1, temp_target_qubit)

    def x(self, qubit_idx):
        """Applies X gate to the specified qubit"""
        x_gate = np.array([[0, 1], [1, 0]])
        x_gate_broadcast = np.kron(
            np.identity(2**qubit_idx),
            np.kron(x_gate, np.identity(2 ** (self.num_qubits - qubit_idx - 1))),
        )
        self.unitary = np.dot(x_gate_broadcast, self.unitary)

    def y(self, qubit_idx):
        """Applies Y gate to the specified qubit"""
        y_gate = np.array([[0, -1j], [1j, 0]])
        y_gate_broadcast = np.kron(
            np.identity(2**qubit_idx),
            np.kron(y_gate, np.identity(2 ** (self.num_qubits - qubit_idx - 1))),
        )
        self.unitary = np.dot(y_gate_broadcast, self.unitary)

    def z(self, qubit_idx):
        """Applies Z gate to the specified qubit"""
        z_gate = np.array([[1, 0], [0, -1]])
        z_gate_broadcast = np.kron(
            np.identity(2**qubit_idx),
            np.kron(z_gate, np.identity(2 ** (self.num_qubits - qubit_idx - 1))),
        )
        self.unitary = np.dot(z_gate_broadcast, self.unitary)

    def h(self, qubit_idx):
        """Applies Hadamard gate to the specified qubit"""
        h_gate = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        h_gate_broadcast = np.kron(
            np.identity(2**qubit_idx),
            np.kron(h_gate, np.identity(2 ** (self.num_qubits - qubit_idx - 1))),
        )
        self.unitary = np.dot(h_gate_broadcast, self.unitary)

    def t(self, qubit_idx):
        """Applies T gate to the specified qubit"""
        t_gate = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]])
        t_gate_broadcast = np.kron(
            np.identity(2**qubit_idx),
            np.kron(t_gate, np.identity(2 ** (self.num_qubits - qubit_idx - 1))),
        )
        self.unitary = np.dot(t_gate_broadcast, self.unitary)

    def tdg(self, qubit_idx):
        """Applies T dag gate (complex conjugatae of T) to the specified qubit"""
        tdg_gate = np.array([[1, 0], [0, np.exp(-1j * np.pi / 4)]])
        tdg_gate_broadcast = np.kron(
            np.identity(2**qubit_idx),
            np.kron(tdg_gate, np.identity(2 ** (self.num_qubits - qubit_idx - 1))),
        )
        self.unitary = np.dot(tdg_gate_broadcast, self.unitary)

    def get_unitary(self):
        """Returns: numpy.ndarray representing unitary matrix of circuit"""
        return self.unitary

    def print_unitary(self):
        """Prints unitary matrix of circuit"""
        print(self.unitary)

    def simulate_run(self, initial_state):
        """Evolves state vector after initial_state is passed through circuit,
        and then simulates a probabilistic measurement of all qubits, returning
        result in decimal. Probabilities are determined by final state vector

        Example:
            qc = LQ3K(2)
            qc.h(0)
            qc.cx(0, 1)
            qc.simulate_run() # returns 0 (0b00) ~50% of time, and 3 (0b11) ~50% of time

        Returns: Integer representation of measured bits
        Raises:
            InvalidStateVector: When initial_state is not unit length."""
        # if initial_state is not unit length, raise InvalidStateVector
        if np.linalg.norm(initial_state) != 1:
            raise self.InvalidStateVector("Initial state is not unit length")
        final_state = self.evolve(initial_state)
        probabilities = np.abs(final_state) ** 2
        return np.random.choice(len(probabilities), p=probabilities)
