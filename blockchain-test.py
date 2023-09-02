import unittest
from blockchain import Blockchain
import blockchain
from hashlib import sha256
from json import dumps

class BlockChainTest(unittest.TestCase):
    
    def test_create_chain(self):
        chain = Blockchain()
        transactions_data = [{"Sender": "test", "Recipient": "test", "Value": "test"}]
        blockchain.create_block(transactions_data, chain)
        keys_test = {"transactions": "", "height": "", "timestamp": "", "prev_hash": "", "nonce": "", "hash": ""}
        self.assertEqual(chain.get()[0].keys(), keys_test.keys(), "Block not created correctly")
    
    def test_proof_of_work(self):
        chain = Blockchain()
        transactions_data = [{"Sender": "test", "Recipient": "test", "Value": "test"}]
        block = {
        "transactions": transactions_data,
        "height": len(chain.get()),
        "timestamp": "test",
        "prev_hash": blockchain.get_prev_hash(chain),
        "nonce": 0,
        }
        difficulty = 4
        proof, _ = blockchain.proof_of_work(block, 4)
        self.assertEqual(proof[:difficulty], "0"*difficulty, 
                         f"Proof of Work should return hash\nthat satisfies the difficulty set by script: currently {'0'*difficulty}")
    
    def test_hash_block(self):
        chain = Blockchain()
        transactions_data = [{"Sender": "test", "Recipient": "test", "Value": "test"}]
        block = {
        "transactions": transactions_data,
        "height": len(chain.get()),
        "timestamp": "test",
        "prev_hash": blockchain.get_prev_hash(chain),
        "nonce": 0,
        }
        my_hash = blockchain.hash_block(block)
        correct_hash = sha256(dumps(block, sort_keys=True).encode('utf8')).hexdigest()
        self.assertEqual(my_hash, correct_hash, "Sha-256 not implemented correctly")
        
if __name__ == "__main__":
    unittest.main()