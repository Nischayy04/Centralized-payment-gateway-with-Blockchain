import hashlib
import json
import os
from datetime import datetime

#note the timestamp that is being stored in other places is done using by converting its integer form to a string
#the timestamp here would be converted into the year month day hour minute second microsecond format 

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

# -------------------------------
#Demo usage
if __name__ == "__main__":
    ledger = BankLedger()
    ledger.load_from_file()

    # Simulated transactions
    ledger.add_transaction("USER001", "MERCHANT123", 500)
    ledger.add_transaction("USER002", "MERCHANT456", 750)
    ledger.add_transaction("USER003", "MERCHANT789", 1000)

    ledger.save_to_file()
    ledger.print_ledger()
    ledger.verify_integrity()
