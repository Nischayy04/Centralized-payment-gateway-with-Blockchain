import hashlib
import time
import random
import json
import os

class Banks:
    def __init__(self, ifsc_code):
        self.ifsc_code = ifsc_code
        self.merchants = []
        self.users = []

    def add_merchant(self, merchant_dict):
        if merchant_dict["ifsc_code"] == self.ifsc_code:
            self.merchants.append(merchant_dict)
        else:
            print(f"[ERROR] IFSC mismatch for merchant '{merchant_dict['name']}'. Expected {self.ifsc_code}, got {merchant_dict['ifsc_code']}")

    def add_user(self, user_dict):
        if user_dict["ifsc_code"] == self.ifsc_code:
            self.users.append(user_dict)
        else:
            print(f"[ERROR] IFSC mismatch for user '{user_dict['name']}'. Expected {self.ifsc_code}, got {user_dict['ifsc_code']}")

# --- ID Generators ---
def generate_merchant_id(name, password):
    timestamp = str(int(time.time()))
    input_string = name + timestamp + password
    return hashlib.sha256(input_string.encode()).hexdigest()[:16]

def generate_user_id(name, password):
    timestamp = str(int(time.time()))
    input_string = name + timestamp + password
    return hashlib.sha256(input_string.encode()).hexdigest()[:16]

def generate_mmid(uid, mobile_number):
    combined = uid + mobile_number
    return hashlib.sha256(combined.encode()).hexdigest()[:16]

# --- Bank Registry ---
bank_registry = {
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

# --- Sample Data ---
def create_sample_data():
    merchant_names = ["MangoMart", "QuickPay", "FlipZon", "Cafe24", "BookHive"]
    user_names = ["Amit", "Riya", "Sameer", "Neha", "Karan"]
    passwords = ["pass123", "secure456", "key789", "lock321", "vault007"]
    mobiles = ["9876543210", "9123456789", "9001122233", "9988776655", "9345678901"]
    bank_codes = list(bank_registry.keys())

    for i in range(5):
        ifsc = random.choice(bank_codes)
        m_name = merchant_names[i]
        u_name = user_names[i]
        pw = passwords[i]
        mob = mobiles[i]

        merchant_mid = generate_merchant_id(m_name, pw)
        user_uid = generate_user_id(u_name, pw)
        user_mmid = generate_mmid(user_uid, mob)

        merchant_data = {
            "name": m_name,
            "ifsc_code": ifsc,
            "password": pw,
            "amount": random.randint(5000, 20000),
            "timestamp": str(int(time.time())),
            "mid": merchant_mid
        }

        user_data = {
            "name": u_name,
            "ifsc_code": ifsc,
            "password": pw,
            "amount": random.randint(2000, 10000),
            "timestamp": str(int(time.time())),
            "uid": user_uid,
            "mobile_number": mob,
            "mmid": user_mmid,
            "pin": "1234"
        }

        # Add to correct bank
        for bank in bank_registry.values():
            bank.add_merchant(merchant_data)
            bank.add_user(user_data)

# --- Save/Load Functions ---
def save_data(filename="bank_data.json"):
    all_data = {}
    for ifsc, bank in bank_registry.items():
        all_data[ifsc] = {
            "merchants": bank.merchants,
            "users": bank.users
        }
    with open(filename, "w") as f:
        json.dump(all_data, f, indent=4)
    print(f"[INFO] Data saved to {filename}")

def load_data(filename="bank_data.json"):
    global bank_registry
    if not os.path.exists(filename):
        print("[INFO] No saved data found. Creating new sample data...")
        create_sample_data()
        save_data(filename)
    else:
        with open(filename, "r") as f:
            all_data = json.load(f)
        for ifsc, data in all_data.items():
            bank = bank_registry.get(ifsc)
            if bank:
                for merchant in data["merchants"]:
                    bank.add_merchant(merchant)
                for user in data["users"]:
                    bank.add_user(user)
        print("[INFO] Loaded data from file.")

# --- Display Helper ---
def print_all_merchants_and_users():
    print("\n--- Merchants and their MIDs ---")
    for bank in bank_registry.values():
        for merchant in bank.merchants:
            print(f"Merchant Name: {merchant['name']} | MID: {merchant['mid']} | IFSC: {merchant['ifsc_code']}")

    print("\n--- Users and their MMIDs ---")
    for bank in bank_registry.values():
        for user in bank.users:
            print(f"User Name: {user['name']} | MMID: {user['mmid']} | IFSC: {user['ifsc_code']}")

# --- Run for testing ---   
if __name__ == "__main__":
    load_data()
    print_all_merchants_and_users()
