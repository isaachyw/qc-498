from qiskit import *
import numpy as np
from qiskit.circuit import *
from qiskit.quantum_info import Statevector

def error_correct() -> Instruction:
    """Returns a circuit (7 code qubits, 3 ancilla bits, 3 classical bits) which
    corrects an arbitrary single-bit error on a Steane encoding
    Aniclla bits should be passed in as |0> and reset back to |0>"""
    
    code = QuantumRegister(7,"code")
    anc = AncillaRegister(3,"anc")
    syn = ClassicalRegister(3,"syn")
    qc = QuantumCircuit(code, anc, syn)
    
    # your code here
        
    return qc.to_instruction(label="EC")
    
def decode_measurement(code: str) -> int:
    """Performs error correction on the passed-in Steane measurement, and
    returns 0 or 1 (int) accordingly based on the resulting logical value
    E.g. decode_measurement("1100001") -> 1 (no correction, valid codeword for 1)
    E.g. decode_measurement("1101001") -> 1 (corrected to 1100001, valid codeword for 1)
    E.g. decode_measurement("1100110") -> 0 (no correction, valid codeword for 0)
    Args:
        code: String corresponding to measurement (most significant bit at LOWER index)"""
    pass


def FT_X() -> Instruction:
    """Returns 7 qubit circuit implementing fault tolerant X gate using Steane code"""
    qc = QuantumCircuit(7)
    # your code here
    return qc.to_instruction(label="FT_X")


def FT_Y() -> Instruction:
    """Returns 7 qubit circuit implementing fault tolerant Y gate using Steane code"""
    qc = QuantumCircuit(7)
    # your code here
    return qc.to_instruction(label="FT_Y")


def FT_Z() -> Instruction:
    """Returns 7 qubit circuit implementing fault tolerant Z gate using Steane code"""
    qc = QuantumCircuit(7)
    # your code here
    return qc.to_instruction(label="FT_Z")

def FT_H() -> Instruction:
    """Returns 7 qubit circuit implementing fault tolerant H gate using Steane code"""
    qc = QuantumCircuit(7)
    # your code here
    return qc.to_instruction(label="FT_H")


def FT_S() -> Instruction:
    """Returns 7 qubit circuit implementing fault tolerant S gate using Steane code"""
    qc = QuantumCircuit(7)
    # your code here
    return qc.to_instruction(label="FT_S")
    
def FT_T() -> Instruction:
    """Returns a circuit (7 code qubits, 7 ancilla bits, 1 classical bit) implementing
    fault tolerant T gate using Steane code
    Aniclla bits should be passed in as |0> and reset back to |0>
    Result should be placed on code qubits"""
    
    code = QuantumRegister(7,"code")
    anc = AncillaRegister(7,"anc")
    cr = ClassicalRegister(1,"meas")
    qc = QuantumCircuit(code, anc, cr)
    
    # your code here
    
    return qc.to_instruction(label="FT_T")


def FT_CX() -> Instruction:
    """Returns 14 qubit circuit implementing fault tolerant CX gate using Steane code
    7 least significant qubits correspond to logical qubit 0 which acts as the control
    7 most significant qubits correspond to logical qubit 1 which acts as the target"""
    qc = QuantumCircuit(14)
    # your code here    
    
    return qc.to_instruction(label="FT_CX")