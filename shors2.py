import numpy as np
from qiskit import QuantumCircuit, execute
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from math import gcd
from fractions import Fraction

# Constants
N = 15
a = 7  # Co-prime with 15

# Step 1: Check if already lucky
if gcd(a, N) != 1:
    print(f"Lucky guess! Found factor: {gcd(a, N)}")
    exit()

n_count = 8  # Number of counting qubits

# Step 2: Quantum Period Finding (uses controlled modular multiplication)

def qpe_amod15(a):
    qc = QuantumCircuit(n_count + 4, n_count)

    # Apply Hadamard to counting qubits
    for q in range(n_count):
        qc.h(q)

    # Initialize 4-qubit target register in |1⟩
    qc.x(n_count + 3)

    # Apply controlled-U^2^j operations
    for q in range(n_count):
        qc.append(c_amod15(a, 2**q), [q] + list(range(n_count, n_count + 4)))

    # Inverse QFT
    qc.append(qft_dagger(n_count), range(n_count))

    # Measurement
    qc.measure(range(n_count), range(n_count))

    # Simulate
    backend = Aer.get_backend('qasm_simulator')
    results = execute(qc, backend, shots=1).result()
    counts = results.get_counts()
    measured = max(counts, key=counts.get)

    # Convert binary to decimal
    phase = int(measured, 2) / (2**n_count)
    print(f"Measured phase: {phase}")

    return phase

# Controlled modular multiplication
def c_amod15(a, power):
    """Controlled multiplication by a^power mod 15"""
    U = QuantumCircuit(4)

    for _ in range(power % 4):
        if a == 7:
            U.swap(0, 1)
            U.swap(1, 2)
            U.swap(2, 3)
        else:
            raise NotImplementedError("Only a = 7 supported")

    U_gate = U.to_gate()
    U_gate.name = f"{a}^{power} mod 15"
    c_U = U_gate.control()
    return c_U

# Inverse QFT
def qft_dagger(n):
    qc = QuantumCircuit(n)
    for qubit in range(n//2):
        qc.swap(qubit, n - qubit - 1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi / 2**(j - m), m, j)
        qc.h(j)
    qc.name = "QFT†"
    return qc

# Run algorithm
phase = qpe_amod15(a)

# Step 3: Estimate r (the period)
frac = Fraction(phase).limit_denominator(N)
r = frac.denominator
print(f"Estimated period r = {r}")

# Step 4: Try to extract factors
if r % 2 != 0:
    print("r is odd; try again.")
    exit()

x = pow(a, r // 2, N)
if x == N - 1:
    print("x = N-1; try again.")
    exit()

factor1 = gcd(x + 1, N)
factor2 = gcd(x - 1, N)

print(f"Factors of {N} are: {factor1} and {factor2}")
