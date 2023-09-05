from os import system, name
from json import dumps
from time import gmtime, asctime
from hashlib import sha256

class Blockchain:
    
    def __init__(self) -> None:
        self.chain: list = []
        self.genesis: str = "0"*64
    
    def get(self) -> list:
        return self.chain
    
    def chain_length(self) -> int:
        return len(self.chain)
    
    def add_block(self, block: dict) -> None:
        self.chain.append(block)

def create_block(transactions: list, blockchain: Blockchain) -> None:
    block = {
        "transactions": transactions,
        "height": len(blockchain.get()),
        "timestamp": asctime(gmtime()),
        "prev_hash": get_prev_hash(blockchain),
        "nonce": 0,
        }
    proof, nonce = proof_of_work(block)
    block["nonce"] = nonce
    block["hash"] = proof
    blockchain.add_block(block)
    

def get_prev_hash(blockchain: Blockchain) -> str:
    if len(blockchain.get()) == 0:
        return blockchain.genesis
    else:
        last_block: dict = blockchain.get()[-1]
        return last_block.get("hash")

def hash_block(block: dict) -> str:
    return sha256(dumps(block, sort_keys=True).encode('utf8')).hexdigest()

def proof_of_work(block: dict, difficulty=4) -> tuple[str, int]:
    nonce = 0
    while True:
        block["nonce"] = nonce
        proof = hash_block(block)
        if proof[:difficulty] == "0" * difficulty:
            return proof, nonce
        nonce += 1

def clear_screen() -> None:
    system("cls" if name == "nt" else "clear")

def create_transaction(sender: str = "", recipient: str = "", value: str = "") -> dict:
    return {
        "sender": sender,
        "recipient": recipient,
        "value": value,
        }

def gather_transactions(chain: Blockchain) -> tuple[dict, int]:
    done = False
    count = 0
    transactions = []
    while not done:
        if count == 0:
            mode = input(f"Do you wish to create a transaction for block {chain.chain_length()}? (y/n): ")
        else:
            mode = input(f"Do you wish to create another transaction for block {chain.chain_length()}? (y/n): ")
        clear_screen()
        if mode == "n":
            done = True
        else:
            count += 1
            print(f"Currently creating transaction number {count} for block with height {chain.chain_length()}.")
            sender = input("Sender: ")
            recipient = input("Recipient: ")
            value = input("Value: ")
            transaction = create_transaction(sender, recipient, value)
            transactions.append(transaction)
            clear_screen()
    return transactions, count

def run(chain: Blockchain) -> None:
    run = True
    while run:
        print(f"Currently creating block with height {chain.chain_length()}")
        transactions, count = gather_transactions(chain)
        print("Creating block and appending to chain...")
        create_block(transactions, chain)
        clear_screen()
        print(f"Block with {count} transactions created!")
        continue_choice = input(f"Do you wish to continue making more blocks? Chain currently has {chain.chain_length()} {'blocks' if chain.chain_length()>1 else 'block'}: (y/n): ")
        if continue_choice == "n":
            run = False
            clear_screen()
    
    format_and_print_json(chain.get())
    
def format_and_print_json(chain:Blockchain):
    for num, block in enumerate(chain):
        print(f"Block {num}")
        print("----------------------")
        for key in block.keys():
            print(f"{key}: {block[key]}")
        print("\t")
    
def main() -> None:
    chain = Blockchain()
    clear_screen()
    print("Welcome to my simple blockchain maker!\nThis terminal program will allow you to create a simple blockchain based on your input and display it.")
   
    while True:
        run(chain)
        mode = input("Do you wish to quit the script (the chain will be lost) or add more blocks? (q to quit/enter to continue): ")
        if mode == "q":
            quit()
        else:
            clear_screen()

if __name__ == "__main__":
    main()
