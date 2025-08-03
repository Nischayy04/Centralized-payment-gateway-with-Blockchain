import socket
import hashlib
import json
import os
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# def load_data(filename="bank_data.pkl"):
#     creating_data.load_data()


class Block:
    def __init__(self, uid, mid, amount, previous_hash):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        self.amount = amount
        self.previous_hash = previous_hash
        self.transaction_id = self.compute_transaction_id(uid, mid)
        self.hash = self.compute_block_hash()

    def compute_transaction_id(self, uid, mid):
        txn_data = f"{uid}{mid}{self.timestamp}{self.amount}".encode()
        return hashlib.sha256(txn_data).hexdigest()

    def compute_block_hash(self):
        block_data = {
            "transaction_id": self.transaction_id,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "amount": self.amount
        }
        return hashlib.sha256(json.dumps(block_data, sort_keys=True).encode()).hexdigest()

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

    @staticmethod
    def from_dict(data):
        block = Block("dummyUID", "dummyMID", data["amount"], data["previous_hash"])
        block.timestamp = data["timestamp"]
        block.transaction_id = data["transaction_id"]
        block.hash = data["hash"]
        return block

class BankLedger:
    def __init__(self):
        self.chain = []

    def create_genesis_block(self):
        genesis_block = Block("SYSTEM", "SYSTEM", 0, "0")
        self.chain.append(genesis_block)

    def add_transaction(self, uid, mid, amount):
        if not self.chain:
            self.create_genesis_block()
        last_block = self.chain[-1]
        new_block = Block(uid, mid, amount, last_block.hash)
        self.chain.append(new_block)

    def print_ledger(self):
        print("\nBlockchain Ledger\n" + "-" * 60)
        for i, block in enumerate(self.chain):
            print(f"Block #{i}")
            print(f"Transaction ID : {block.transaction_id}")
            print(f"Timestamp      : {block.timestamp}")
            print(f"Amount         : ₹{block.amount}")
            print(f"Previous Hash  : {block.previous_hash}")
            print(f"Block Hash     : {block.hash}")
            print("-" * 60)

    def save_to_file(self, filename="upi_ledger.json"):
        chain_data = [block.to_dict() for block in self.chain]
        with open(filename, "w") as f:
            json.dump(chain_data, f, indent=4)

    def load_from_file(self, filename="upi_ledger.json"):
        if not os.path.exists(filename):
            print("Ledger file not found. Creating genesis block.")
            self.create_genesis_block()
            return

        with open(filename, "r") as f:
            chain_data = json.load(f)
        self.chain = [Block.from_dict(b) for b in chain_data]

    def verify_integrity(self):
        print("\nVerifying blockchain integrity...")
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            recalculated_hash = current.compute_block_hash()
            if current.hash != recalculated_hash:
                print(f"[ERROR] Block #{i} hash mismatch!")
                return False

            if current.previous_hash != previous.hash:
                print(f"[ERROR] Block #{i} has incorrect previous hash!")
                return False

        print("[SUCCESS] Blockchain integrity verified. All hashes are valid.")
        return True

def load_bank_private_key():
    with open("bank_private.pem", "rb") as f:
        private_key = RSA.import_key(f.read())
    return PKCS1_OAEP.new(private_key)

def load_bank_data(filename="bank_data.json"):
    if not os.path.exists(filename):
        print("[ERROR] bank_data.json not found.")
        return None, None

    f = open(filename, "r+")
    data = json.load(f)
    return data, f

# def verify_transaction(sent_mmid, sent_pin, sent_amount, sent_mid, ledger):
#     user_found = None
#     merchant_found = None

#     for bank in creating_data.bank_registry.values():         #search for user
#         for user in bank.users:
#             if user.mmid == sent_mmid:
#                 user_found = user
#                 break
#         if user_found:
#             break

#     if not user_found:
#         return False, "MMID not found"

#     if user_found.password != sent_pin:
#         return False, "Incorrect PIN"

#     if user_found.amount < sent_amount:
#         return False, "Insufficient balance"

#     user_found.amount -= sent_amount

#     for bank in creating_data.bank_registry.values():          #search for merchant
#         for merchant in bank.merchants:
#             if merchant.mid == sent_mid:
#                 merchant_found = merchant
#                 break
#         if merchant_found:
#             break

#     if not merchant_found:
#         return False, "Merchant ID not found"

#     merchant_found.amount += sent_amount

#     # Add transaction to the blockchain ledger
#     ledger.add_transaction(user_found.uid, merchant_found.mid, sent_amount)
#     ledger.save_to_file()

#     return True, "Transaction successful"

# def verify_transaction(mmid, pin, amount, mid, ledger, bank_data):
#     user_found = None
#     merchant_found = None

#     for bank in bank_data.values():
#         for user in bank["users"]:
#             if user["mmid"] == mmid:
#                 user_found = user
#                 break
#         if user_found:
#             break

#     if not user_found:
#         return False, "MMID not found"

#     if user_found["pin"] != pin:
#         return False, "Incorrect PIN"

#     if user_found["amount"] < amount:
#         return False, "Insufficient balance"

#     user_found["amount"] -= amount

#     for bank in bank_data.values():
#         for merchant in bank["merchants"]:
#             if merchant["mid"] == mid:
#                 merchant_found = merchant
#                 break
#         if merchant_found:
#             break

#     if not merchant_found:
#         return False, "Merchant ID not found"

#     merchant_found["amount"] += amount

#     ledger.add_transaction(user_found["uid"], merchant_found["mid"], amount)
#     ledger.save_to_file()

#     return True, "Transaction successful"

def verify_transaction(mmid, pin, amount, mid, ledger, bank_data, file_handle):
    user_found = None
    merchant_found = None

    # Find user
    for bank in bank_data.values():
        for user in bank["users"]:
            if user["mmid"] == mmid:
                user_found = user
                break
        if user_found:
            break

    if not user_found:
        return False, "MMID not found"

    if user_found["pin"] != pin:
        return False, "Incorrect PIN"

    if user_found["amount"] < amount:
        return False, "Insufficient balance"

    user_found["amount"] -= amount

    # Find merchant
    for bank in bank_data.values():
        for merchant in bank["merchants"]:
            if merchant["mid"] == mid:
                merchant_found = merchant
                break
        if merchant_found:
            break

    if not merchant_found:
        return False, "Merchant ID not found"

    merchant_found["amount"] += amount

    # Move to beginning and overwrite the updated data
    file_handle.seek(0)
    json.dump(bank_data, file_handle, indent=4)
    file_handle.truncate()  # Ensure old data is cleared if new content is shorter
    file_handle.flush()

    # Add transaction to blockchain
    ledger.add_transaction(user_found["uid"], merchant_found["mid"], amount)
    ledger.save_to_file()

    return True, "Transaction successful"

# --- Bank Client Config ---
UPI_MACHINE_IP = '192.168.191.192'   # IP of UPI Machine
UPI_MACHINE_PORT = 7000            # Port where UPI machine expects bank messages

def start_bank_client(ledger, bank_data):

    try:
        # Connect to UPI Machine
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2000)
        sock.connect((UPI_MACHINE_IP, UPI_MACHINE_PORT))
        print("[BANK] Connected to UPI Machine")

        # Wait for a message (blocking)
        data = sock.recv(4096)
        #print("[BANK] Received transaction data:", data)

        bank_cipher = load_bank_private_key()
        decrypted_data = bank_cipher.decrypt(data).decode()

        parts = decrypted_data.split(";")
        mmid = parts[0]
        pin = parts[1]
        amount = float(parts[2])
        mid = parts[3]
        #print(f"[BANK] MMID: {mmid}, PIN: {pin}, Amount: {amount}, MID: {mid}")

        transaction_message = verify_transaction(mmid, pin, amount, mid, ledger, bank_data, bank_file)

        # Simulate transaction verification and reply

        if transaction_message[0]:
            response = "BANK:Successful Transaction"
        else:
            response = f"BANK:Transaction Failed - {transaction_message[1]}"
            
        sock.send(response.encode())
        print("[BANK] Sent response back to UPI Machine")
        sock.close()

    except Exception as e:
        print("[BANK ERROR]", e)

if __name__ == "__main__":
    ledger = BankLedger()
    ledger.load_from_file()

    bank_data, bank_file = load_bank_data()

    start_bank_client(ledger, bank_data)
