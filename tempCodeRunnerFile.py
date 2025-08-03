
import numpy as np
from qiskit import Aer
from qiskit.algorithms import Shor
from qiskit.utils import QuantumInstance
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# def convert_pin_to_rsa_number(pin, mmid):
#     """
#     Convert PIN and MMID to an RSA-like number for demonstration purposes.
#     """
#     combined = str(pin) + str(mmid)
#     hash_object = hashlib.sha256(combined.encode())
#     hash_hex = hash_object.hexdigest()
    
#     # Take first 8 characters of hex and convert to integer
#     return int(hash_hex[:8], 16)

def load_upi_public_key():
    with open("upi_public.pem", "rb") as f:
        key = RSA.import_key(f.read())
    return PKCS1_OAEP.new(key)



def quantum_factor_pin(pin, mmid):
    """
    Use Shor's algorithm to factor a number derived from PIN and MMID
    """
    # Convert PIN and MMID to a demonstration "secure" number

    message = str(pin) + str(mmid)
    cipher = load_upi_public_key()
    rsa_num = cipher.encrypt(message.encode())

    # rsa_like_number = convert_pin_to_rsa_number(pin, mmid)
    
    # For demonstration - use a smaller number derived from the original
    # Real Shor's algorithm needs thousands of qubits for actual RSA numbers
    demo_n = rsa_num % 15
    if demo_n % 2 == 0 or demo_n <= 2:  # Ensure we have an odd number > 2 for the demo
        demo_n = 15  # Use 15 as default (factors: 3, 5)
    
    # Set up the quantum instance (simulator)
    backend = Aer.get_backend('aer_simulator')
    quantum_instance = QuantumInstance(backend)
    
    # Run Shor's algorithm
    try:
        shor = Shor(quantum_instance=quantum_instance)
        result = shor.factor(demo_n)
        return result.factors
    except Exception as e:
        return f"Error running Shor's algorithm: {e}"

if __name__ == "__main__":
    # Sample credentials to test
    sample_pin = "1234"  # 4-digit PIN
    sample_mmid = "129fa251298e0640"  # 9-digit MMID
    
    # Get the factors using Shor's algorithm
    factors = quantum_factor_pin(sample_pin, sample_mmid)
    print(f"Factors found: {factors}")