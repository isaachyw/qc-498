from qiskit import *
from qiskit.circuit import *
from qiskit.circuit.library.standard_gates import MCXGate
from qiskit.visualization import plot_histogram

from qiskit.quantum_info import Statevector
import numpy as np

import sys

import math
import csv

import counter, grover, oracle

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: ./%s [csv_file]" % sys.argv[0])
    driver = Driver(sys.argv[1])
    if driver.run_search():
        driver.print_solution()
    else:
        print("GROVER: No solution found after %d attempts" % MAX_SEARCHES)



if __name__ == "__main__":
    main()

