import time
import binascii

def rol(x, r, n_bits=16):
    """Rotate left operation for 16-bit word size"""
    return ((x << r) | (x >> (n_bits - r))) & ((1 << n_bits) - 1)

def ror(x, r, n_bits=16):
    """Rotate right operation for 16-bit word size"""
    return ((x >> r) | (x << (n_bits - r))) & ((1 << n_bits) - 1)

class SPECK_LWC:
    """
    Lightweight implementation of SPECK block cipher
    Using 32-bit plaintext (two 16-bit words) and 64-bit key
    """
    def __init__(self, key, rounds=10):
        """
        Initialize SPECK_LWC cipher
        
        Args:
            key (str or bytes): 8-byte (64-bit) encryption key
            rounds (int): Number of rounds (10 for this implementation)
        """
        self.rounds = rounds
        self.word_size = 16  # 16-bit word size for 32-bit total plaintext
        
        # Convert key to bytes if it's a string
        if isinstance(key, str):
            key = key.encode('utf-8')
        
        # Ensure key is exactly 8 bytes (64 bits)
        if len(key) != 8:
            raise ValueError("Key must be exactly 8 bytes (64 bits)")
        
        # Store the original key
        self.original_key = key
            
        # Generate round keys
        self.round_keys = self._expand_key(key)
    
    def _expand_key(self, key):
        """
        Generate round keys from master key
        For 64-bit key (8 bytes) with 16-bit word size
        """
        # Convert the key to integer
        key_int = int.from_bytes(key, byteorder='little')
        
        # Split key into four 16-bit parts
        k = [
            (key_int >> (16 * i)) & 0xFFFF 
            for i in range(4)
        ]
        
        # SPECK key schedule for 16-bit words
        l = k[1:]  # [k1, k2, k3]
        round_keys = [k[0]]  # Start with k0
        
        for i in range(self.rounds - 1):
            l[0] = (ror(l[0], 7, self.word_size) + round_keys[i]) % (1 << self.word_size) ^ i
            round_keys.append(l[0])
            l = l[1:] + [l[0]]  # Rotate l
        
        return round_keys
    
    def encrypt(self, plaintext):
        """
        Encrypt a 4-byte (32-bit) plaintext using SPECK
        
        Args:
            plaintext (bytes or str): 4-byte plaintext to encrypt
            
        Returns:
            bytes: 4-byte encrypted data
        """
        # Convert plaintext to bytes if it's a string
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        
        # Ensure plaintext is exactly 4 bytes (32 bits)
        if len(plaintext) != 4:
            raise ValueError("Plaintext must be exactly 4 bytes (32 bits)")
        
        # Print detailed plaintext and key information just before encryption
        print("\n--- ENCRYPTION DEBUG INFO ---")
        print(f"Plaintext (raw bytes): {plaintext}")
        print(f"Plaintext (ASCII): '{plaintext.decode('utf-8', errors='replace')}'")
        print(f"Plaintext (hex): {plaintext.hex()}")
        print(f"Plaintext (decimal): {int.from_bytes(plaintext, byteorder='little')}")
        
        print(f"Key (raw bytes): {self.original_key}")
        print(f"Key (ASCII): '{self.original_key.decode('utf-8', errors='replace')}'")
        print(f"Key (hex): {self.original_key.hex()}")
        print(f"Key (decimal): {int.from_bytes(self.original_key, byteorder='little')}")
        print("--- END DEBUG INFO ---\n")
        
        # Convert plaintext to integer
        plaintext_int = int.from_bytes(plaintext, byteorder='little')
        
        # Split into two 16-bit words
        b = plaintext_int & 0xFFFF        # Lower 16 bits
        a = (plaintext_int >> 16) & 0xFFFF  # Upper 16 bits
        
        # Apply SPECK encryption rounds
        for i in range(self.rounds):
            a = (ror(a, 7, self.word_size) + b) % (1 << self.word_size) ^ self.round_keys[i]
            b = rol(b, 2, self.word_size) ^ a
        
        # Combine the two parts
        result = (a << 16) | b
        
        # Convert back to bytes
        return result.to_bytes(4, byteorder='little')


def generate_mid_to_vmid(mid):
    """
    Convert Merchant ID to Virtual Merchant ID using SPECK LWC algorithm
    with 32-bit plaintext and 64-bit key
    
    Args:
        mid (str): Merchant ID
        
    Returns:
        dict: Payment data with MID, VMID, and timestamp
    """
    # Generate timestamp for key derivation
    timestamp = int(time.time())
    
    # Create key using timestamp as specified
    key = f"UPI{timestamp}"[:8].ljust(8)  # Ensure exactly 8 bytes
    print(f"Timestamp: {timestamp}")
    print(f"Encryption Key: {key} ({len(key)} bytes)")
    
    # Take only first 4 characters of MID (32 bits)
    mid_truncated = mid[:4]
    if len(mid_truncated) < 4:
        mid_truncated = mid_truncated.ljust(4)  # Pad to 4 bytes if needed
    
    print(f"Original MID: {mid}")
    print(f"Truncated MID (for encryption): {mid_truncated} (4 bytes/32 bits)")
    
    # Initialize SPECK cipher with 10 rounds
    cipher = SPECK_LWC(key)
    
    # Encrypt the MID
    encrypted = cipher.encrypt(mid_truncated)
    
    # Convert to hexadecimal
    vmid = encrypted.hex()
    
    print(f"Encrypted VMID (hex): {vmid} (8 hex chars representing 32 bits)")
    
    # Create payment data JSON
    payment_data = {
        "mid": mid,
        "vmid": vmid,
        "timestamp": str(timestamp)
    }
    
    return payment_data


# Example usage
if __name__ == "__main__":
    # Example Merchant ID
    merchant_id = "MERCHANT123456789"
    
    # Generate VMID and payment data
    payment_data = generate_mid_to_vmid(merchant_id)
    
    # Display payment data
    print("\nPayment Data JSON:")
    for key, value in payment_data.items():
        print(f"  \"{key}\": \"{value}\"")