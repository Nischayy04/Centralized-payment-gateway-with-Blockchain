import hashlib
import time
import random
import pickle
import os

class Banks:
    def __init__(self, ifsc_code):
        self.ifsc_code = ifsc_code
        self.merchants = []       #list of merchants in the bank branch
        self.users = []           #list of users in the bank branch  

    def add_merchant(self, merchant):
        if merchant.ifsc_code == self.ifsc_code:
            self.merchants.append(merchant)
            #print(f"[BANK] Merchant '{merchant.name}' added to branch {self.ifsc_code}.")
        else:
            print("[BANK] IFSC mismatch — merchant not added.")

    def add_user(self, user):
        if user.ifsc_code == self.ifsc_code:
            self.users.append(user)
            #print(f"[BANK] User '{user.name}' added to branch {self.ifsc_code}.")
        else:
            print("[BANK] IFSC mismatch — user not added.")

class Merchants:
    def __init__(self, name, ifsc_code, password, amount):
        self.name = name
        self.ifsc_code = ifsc_code
        self.password = password
        self.amount = amount
        self.timestamp = str(int(time.time())) #stored as a string to ensure consistency and so that it can be concatenated easily
        self.mid = generate_merchant_id(name, password) 

        bank = bank_registry.get(ifsc_code)             #adds merchant instance to the right bank branch
        if bank:
            bank.add_merchant(self)
        else:
            print(f"[ERROR] No bank found with IFSC: {ifsc_code}")

class Users:
    def __init__(self, name, ifsc_code, password, amount, mobile_number, pin):
        self.name = name
        self.ifsc_code = ifsc_code
        self.password = password
        self.amount = amount
        self.timestamp = str(int(time.time())) #stored as a string
        self.uid = generate_user_id(name, password) 
        self.mobile_number = mobile_number
        self.mmid = generate_mmid(self.uid, mobile_number)
        self.pin = pin

        bank = bank_registry.get(ifsc_code)    #adds user instance to the right bank branch
        if bank:
            bank.add_user(self)
        else:
            print(f"[ERROR] No bank found with IFSC: {ifsc_code}")

def save_data(filename="bank_data.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(bank_registry, f)

def load_data(filename="bank_data.pkl"):
    global bank_registry
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            bank_registry = pickle.load(f)
        print("[INFO] Loaded data from file.")
    else:
        print("[INFO] No saved data found. Creating fresh sample data...")
        create_sample_data()
        save_data()

bank_registry = {                           #maintains a list of banks and their ifsc codes, which are 11 digits long
    "SBIN0000001": Banks("SBIN0000001"),    
    "SBIN0000002": Banks("SBIN0000002"),
    "SBIN0000003": Banks("SBIN0000003"),
    "ICIC0000001": Banks("ICIC0000001"),
    "ICIC0000002": Banks("ICIC0000002"),
    "ICIC0000003": Banks("ICIC0000003"),
    "HDFC0000001": Banks("HDFC0000001"),
    "HDFC0000002": Banks("HDFC0000002"),
    "HDFC0000003": Banks("HDFC0000003")
}

def generate_merchant_id(name, password):   #generates a 16 digit merchant id using name, timestamp and password by sha256 hashing
    timestamp = str(int(time.time()))
    input_string = name + timestamp + password
    
    input_bytes = input_string.encode('utf-8')  # Convert to bytes for hashing
    
    hash_object = hashlib.sha256(input_bytes)   # Generate SHA-256 hash
    hash_hex = hash_object.hexdigest()
    
    merchant_id = hash_hex[:16]    # Take the first 16 characters of hash
    
    return merchant_id

def generate_user_id(name, password):      #16 digit user id generation using name, timestamp and password by sha256 hashing
    timestamp = str(int(time.time()))
    input_string = name + timestamp + password
    
    input_bytes = input_string.encode('utf-8')
    
    hash_object = hashlib.sha256(input_bytes)
    hash_hex = hash_object.hexdigest()
    
    user_id = hash_hex[:16]
    
    return user_id

def generate_mmid(uid, mobile_number):       #16 digit mmid generation using uid and mobile number by sha256 hashing
    combined = uid + mobile_number
    
    hash_object = hashlib.sha256(combined.encode('utf-8')) # Convert to bytes for hashing
    hash_hex = hash_object.hexdigest()
    mmid = hash_hex[:16] #taking first 16 bytes of the hash
    
    return mmid

def create_sample_data():
    merchant_names = ["MangoMart", "QuickPay", "FlipZon", "Cafe24", "BookHive"]
    user_names = ["Amit", "Riya", "Sameer", "Neha", "Karan"]
    passwords = ["pass123", "secure456", "key789", "lock321", "vault007"]
    mobiles = ["9876543210", "9123456789", "9001122233", "9988776655", "9345678901"]
    bank_codes = list(bank_registry.keys())

    for i in range(5):
        m_name = merchant_names[i]
        u_name = user_names[i]
        pw = passwords[i]
        mob = mobiles[i]
        ifsc = random.choice(bank_codes)

        Merchants(name=m_name, ifsc_code=ifsc, password=pw, amount=random.randint(5000, 20000))
        Users(name=u_name, ifsc_code=ifsc, password=pw, amount=random.randint(2000, 10000), mobile_number=mob, pin=1234)

def print_all_merchants_and_users():
    print("\n--- Merchants and their MIDs ---")
    for bank in bank_registry.values():
        for merchant in bank.merchants:
            print(f"Merchant Name: {merchant.name} | MID: {merchant.mid} | IFSC: {merchant.ifsc_code}")

    print("\n--- Users and their MMIDs ---")
    for bank in bank_registry.values():
        for user in bank.users:
            print(f"User Name: {user.name} | MMID: {user.mmid} | IFSC: {user.ifsc_code}")


if __name__ == "__main__":
    load_data()
    print_all_merchants_and_users()