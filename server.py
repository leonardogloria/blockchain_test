from blockchain import Blockchain
import sys
import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
import requests
from urllib.parse import urlparse
app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()

@app.route('/blockchain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain) 
    }
    return jsonify(response), 200
@app.route('/mine',methods=['GET'])
def mine_block():
    blockchain.add_transactions(sender="0", recipient= node_identifier, amount=1)
    last_block_hash = blockchain.hash_block(blockchain.last_block)
    index = len(blockchain.chain)
    nonce = blockchain.proof_of_work(index,last_block_hash,blockchain.current_transactions)
    block = blockchain.append_block(nonce,last_block_hash)
    response = { 
        'message': "New Block Mined",
        'index': block['index'],
        'hash_of_previous_block': block['hash_of_previous_block'],
        'nonce': block['nonce']
        #'transactions': block['transactions'],
    }
    return jsonify(response), 200
@app.route('/transactions/new', methods=['POST'])    
def new_transaction():
    values = request.get_json()
    required_fields = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required_fields):
        return ('Missing Fields', 400)
    index = blockchain.add_transactions(
        values['sender'],
        values['recipient'],
        values['amount']
    )
    response = { 
        'message': f'Transaction will be added to Block{index}'} 
        
    
    return (jsonify(response),201)


if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=int(sys.argv[1]))
