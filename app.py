# save this as app.py
from flask import Flask, jsonify, request
from markupsafe import escape
import blockchain

app = Flask(__name__)
node = blockchain.Blockchain()

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/transactions/create', methods=['POST'])
def create_transaction():
    data = request.json
    
    if data is not None:
        transaction = node.createTransaction(data["sender"], data["recipient"], data["amount"], data["timestamp"], data["privWifKey"])
        return jsonify({"message": "Sucess", "transaction": transaction}), 201

    return jsonify({"message": "Error"}), 400    

@app.route('/transactions/mempool', methods=['GET'])
def get_mempool():
    return node.memPool

@app.route('/mine', methods=['GET'])
def mine():
    return node.createBlock()

@app.route('/chain', methods=['GET'])
def get_chain():
    return node.chain

@app.route('/nodes/register', methods=['POST'])
def register_node():
    data = request.json

    if len(data) == 1: # 1 URL por vez
        node.nodes.add(str(data['url'])) 
        return jsonify({"message": "Sucess", "nodes": list(node.nodes)}), 201
    return jsonify({"message": "Error"}), 201

@app.route('/nodes/resolve', methods=['GET'])
def resolve():
    # [GET] /nodes/resolve para executar o modelo de consenso, 
    # resolvendo conflitos e garantindo que contém a cadeia de blocos correta.
    # Basicamente o que deve ser feito pelo nó é solicitar a todos os seus nós registrados os seus respectivos blockchains.
    # Então deve-se conferir se o blockchain é válido, e, se for maior (mais longo) que o atual, deve substitui-lo.
    return node.resolveConflicts()


if __name__ == '__main__':
    import argparse

    # para executar: python3 app.py --port 5001(num da porta)

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5000, help="Port to run the Flask app")
    args = parser.parse_args()    
    app.run(port=args.port)