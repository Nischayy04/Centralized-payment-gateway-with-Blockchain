import hashlib
import time

def generate_user_id(name, password):      #16 digit user id generation using name, timestamp and password by sha256 hashing
    timestamp = str(int(time.time()))
    input_string = name + timestamp + password
    
    # Convert to bytes for hashing
    input_bytes = input_string.encode('utf-8')
    
    # Generate SHA-256 hash
    hash_object = hashlib.sha256(input_bytes)
    hash_hex = hash_object.hexdigest()
    
    # Take the first 16 characters of the hexadecimal hash
    user_id = hash_hex[:16]
    
    return user_id

def generate_mmid(uid, mobile_number):       #16 digit mmid generation using uid and mobile number by sha256 hashing
    combined = uid + mobile_number
    
    hash_object = hashlib.sha256(combined.encode('utf-8')) # Convert to bytes for hashing
    hash_hex = hash_object.hexdigest()
    mmid = hash_hex[:16] #taking first 16 bytes of the hash
    
    return mmid

# Example usage
if __name__ == "__main__":
    user_name = input("Enter user name: ")
    user_password = input("Enter user password: ")
    mobile_number = input("Enter mobile number: ")
    
    uid = generate_user_id(user_name, user_password)
    mmid = generate_mmid(uid, mobile_number)
    
    print(f"Generated User ID (UID): {uid}")
    print(f"Generated Mobile Money Identifier (MMID): {mmid}")