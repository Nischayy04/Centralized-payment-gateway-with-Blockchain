import time

def rol(x, r, n_bits=64):
    """Rotate left operation for 64-bit word size"""
    return ((x << r) | (x >> (n_bits - r))) & ((1 << n_bits) - 1)

def ror(x, r, n_bits=64):
    """Rotate right operation for 64-bit word size"""
    return ((x >> r) | (x << (n_bits - r))) & ((1 << n_bits) - 1)

def encrypt_mid(mid):
    
    # Generate timestamp for key derivation
    timestamp = int(time.time())
    
    # Create key using timestamp - 16 bytes for 64-bit word size (2 words)
    key = f"UPI{timestamp}KEY".ljust(16)
    
    # Take up to 16 characters of MID (128 bits) for 64-bit word size
    mid_truncated = mid[:16].ljust(16)  # Pad to 16 bytes if needed
    
    # Encrypt using SPECK cipher with 64-bit word size
    word_size = 64
    rounds = 27  # Standard rounds for Speck64/128
    
    # Convert key to bytes if it's a string
    if isinstance(key, str):
        key = key.encode('utf-8')
    
    # Convert plaintext to bytes if it's a string
    if isinstance(mid_truncated, str):
        mid_truncated = mid_truncated.encode('utf-8')
    
    # Generate round keys - for 64-bit word size, 16-byte key
    key_int = int.from_bytes(key, byteorder='little')
    k = [(key_int >> (64 * i)) & ((1 << 64) - 1) for i in range(2)]
    l = k[1:]  # [k1]  # noqa: E741
    round_keys = [k[0]]  # Start with k0
    
    for i in range(rounds - 1):
        l[0] = (ror(l[0], 8, word_size) + round_keys[i]) % (1 << word_size) ^ i
        round_keys.append(l[0])
        # Note: With only 2 key words, we don't need to rotate l
    
    # Encrypt plaintext with 64-bit word size
    plaintext_int = int.from_bytes(mid_truncated, byteorder='little')
    b = plaintext_int & ((1 << 64) - 1)          # Lower 64 bits
    a = (plaintext_int >> 64) & ((1 << 64) - 1)  # Upper 64 bits
    
    # Apply encryption rounds
    for i in range(rounds):
        a = (ror(a, 8, word_size) + b) % (1 << word_size) ^ round_keys[i]
        b = rol(b, 3, word_size) ^ a
    
    # Combine the two parts
    result = (a << 64) | b
    
    # Convert to hex string
    vmid = result.to_bytes(16, byteorder='little').hex()
    
    return {"vmid": vmid, "timestamp": timestamp}

def decrypt_vmid(vmid, timestamp):
    
    # Convert timestamp to integer if needed
    if isinstance(timestamp, str):
        timestamp = int(timestamp)
    
    # Create key using provided timestamp - 16 bytes for 64-bit word size
    key = f"UPI{timestamp}KEY".ljust(16)
    key = key.encode('utf-8')
    
    # Convert VMID from hex to bytes
    vmid_bytes = bytes.fromhex(vmid)
    
    # Set up constants
    word_size = 64
    rounds = 27
    
    # Generate round keys
    key_int = int.from_bytes(key, byteorder='little')
    k = [(key_int >> (64 * i)) & ((1 << 64) - 1) for i in range(2)]
    l = k[1:]  # [k1]  # noqa: E741
    round_keys = [k[0]]  # Start with k0
    
    for i in range(rounds - 1):
        l[0] = (ror(l[0], 8, word_size) + round_keys[i]) % (1 << word_size) ^ i
        round_keys.append(l[0])
        # No rotation needed with only 2 key words
    
    # Decrypt ciphertext with 64-bit word size
    ciphertext_int = int.from_bytes(vmid_bytes, byteorder='little')
    b = ciphertext_int & ((1 << 64) - 1)          # Lower 64 bits
    a = (ciphertext_int >> 64) & ((1 << 64) - 1)  # Upper 64 bits
    
    # Apply decryption rounds (reverse order)
    for i in range(rounds - 1, -1, -1):
        b = ror(a ^ b, 3, word_size)
        a = rol(((a ^ round_keys[i]) - b) % (1 << word_size), 8, word_size)
    
    # Combine the two parts
    result = (a << 64) | b
    
    # Convert back to string
    try:
        mid = result.to_bytes(16, byteorder='little').decode('utf-8')
    except UnicodeDecodeError:
        # If can't decode as UTF-8, return hex representation
        mid = result.to_bytes(16, byteorder='little').hex()
    
    return mid

# Example usage
if __name__ == "__main__":
    # Encrypt
    merchant_id = "MERCHANT123456789"
    encrypted = encrypt_mid(merchant_id)
    
    # Decrypt
    vmid = encrypted["vmid"]
    timestamp = encrypted["timestamp"]
    recovered_mid = decrypt_vmid(vmid, timestamp)
    
    # Verify
    print(f"Original MID (first 16 chars): {merchant_id[:16]}")
    print(f"Recovered MID: {recovered_mid}")
    print(f"MIDs match: {recovered_mid.strip() == merchant_id[:16].strip()}")