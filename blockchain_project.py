import datetime
import json
import hashlib
from operator import truediv
from flask import Flask, jsonify
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_blockchain(proof_of_work = 1, previous_hash = '0', current_hash = '000000000019d8869c085ae165821e923ff793ae46a2a6c172b3f1b60a8ce26f')
    def create_blockchain(self, proof_of_work, previous_hash, current_hash):       
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof_of_work': proof_of_work,
            'current_hash': current_hash
        }
        self.chain.append(block)
        return block
    def get_previous_block(self):
        last_block = self.chain[-1]
        return last_block
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof= True
            else:
                new_proof += 1
        return new_proof
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof_of_work']
            current_proof = block['proof_of_work']
            hash_operation = hashlib.sha256(str(current_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
app = Flask(__name__) 
blockchain = Blockchain()
@app.route('/mine_a_block', methods = ['GET'])
def mine_a_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof_of_work']
    proof_0f_work = blockchain.proof_of_work(previous_proof)
    previous_hash = previous_block['current_hash']
    current_hash = blockchain.hash(previous_block)
    block = blockchain.create_blockchain(proof_0f_work, previous_hash, current_hash,)
    response = {'message': 'congratulations, You have Successfully Mined a New Block!!!', 'index': block['index'], 'timestamp': block['timestamp'],'proof_of_work': block['proof_of_work'], 'previous_hash': block['previous_hash'], 'current_hash': block['current_hash'] }
    return jsonify(response), 200
@app.route('/get_complete_chain', methods = ['GET'])
def get_complete_chain():
    response = {'chain': blockchain.chain, 'lenght': len(blockchain.chain)}
    return jsonify(response), 200
@app.route('/is_blockchain_valid', methods = ['GET'])
def is_blockchain_valid():
    valid = blockchain.is_chain_valid(blockchain.chain)
    if valid:
        response = {'message': 'Yes, The Blockchain is valid.'}
    else:
        response = {'message': 'No, The Blockchain is not valid.'}
    return jsonify(response), 200
app.run(debug = True, host = '0.0.0.0', port = 5000)
        