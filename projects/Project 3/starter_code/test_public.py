import unittest

from qiskit.circuit import *

from typing import Dict


import p3, execute

class TestPublic(unittest.TestCase):
    

    def test_decode(self):
        self.assertEqual(p3.decode_measurement("1100001"),1)
        self.assertEqual(p3.decode_measurement("1101001"),1)

    def test_bitflip_correction(self):

        # create circuit
        code = QuantumRegister(7, 'code')
        anc = QuantumRegister(3, 'ancilla')
        results = ClassicalRegister(7, 'result')
        qc = QuantumCircuit(code,anc, results)

        # error correction maps state to |0>_L
        # attach to all code and ancilla qubits, and 3 classical bits
        qc.append(p3.error_correct(), code[:] + anc[:], results[0:3])

        # add random bit-flip error
        qc.x(3)

        # map |0>_L to |1>_L and error correct
        qc.append(p3.FT_X(), code)
        qc.append(p3.error_correct(), code[:] + anc[:], results[0:3])

        
        # add random bit-flip error
        qc.x(2)
        
        # map |1>_L to |0>_L and error correct
        qc.append(p3.FT_X(), code)
        qc.append(p3.error_correct(), code[:] + anc[:], results[0:3])


        # measure results and run simulations
        qc.measure(code, results)
        counts = execute.run_sim(qc.copy(), 100)

        # ensure every result corresponds to a valid 0 state
        # (after error correction)
        for result in list(counts):
            trimmed_result = result.replace(" ","")
            self.assertEqual(p3.decode_measurement(trimmed_result),0)
            
if __name__ == "__main__":
	unittest.main()