import hashlib
import time

def generate_merchant_id(name, password):
    """
    Generate a 16-digit Merchant ID (MID) using:
    - Merchant's name
    - Current timestamp (time of account creation)
    - Password
    
    The function uses SHA-256 algorithm to hash these inputs and 
    converts it to a 16-digit hexadecimal number.
    
    Args:
        name (str): Merchant's name
        password (str): Merchant's password
        
    Returns:
        str: 16-digit hexadecimal Merchant ID
    """
    # Get current timestamp
    timestamp = str(int(time.time()))
    
    # Combine inputs for hashing
    input_string = name + timestamp + password
    
    # Convert to bytes for hashing
    input_bytes = input_string.encode('utf-8')
    
    # Generate SHA-256 hash
    hash_object = hashlib.sha256(input_bytes)
    hash_hex = hash_object.hexdigest()
    
    # Take the first 16 characters of the hexadecimal hash
    merchant_id = hash_hex[:16]
    
    return merchant_id

# Example usage
if __name__ == "__main__":
    merchant_name = input("Enter merchant name: ")
    merchant_password = input("Enter merchant password: ")
    
    mid = generate_merchant_id(merchant_name, merchant_password)
    print(f"Generated Merchant ID (MID): {mid}")