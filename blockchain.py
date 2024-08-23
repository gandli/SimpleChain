from flask import Flask, jsonify, request, render_template
import hashlib
import json
from time import time
import os
from datetime import datetime


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.load_data()  # 加载数据

    def load_data(self):
        """从文件加载区块链数据"""
        if os.path.exists("blockchain_data.json"):
            try:
                with open("blockchain_data.json", "r") as file:
                    data = json.load(file)
                    if data:  # 检查文件是否为空
                        self.chain = data.get("chain", [])
                        self.current_transactions = data.get("current_transactions", [])
                    else:
                        print("blockchain_data.json 文件为空，创建创世区块...")
                        self.new_block(previous_hash="1", proof=100)
            except json.JSONDecodeError:
                print("blockchain_data.json 文件损坏或格式错误，创建创世区块...")
                self.new_block(previous_hash="1", proof=100)
        else:
            # 如果文件不存在，创建创世区块
            print("blockchain_data.json 文件不存在，创建创世区块...")
            self.new_block(previous_hash="1", proof=100)

    def save_data(self):
        """将区块链数据保存到文件"""
        data = {"chain": self.chain, "current_transactions": self.current_transactions}
        with open("blockchain_data.json", "w") as file:
            json.dump(data, file, indent=4)

    def new_block(self, proof, previous_hash=None):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        self.save_data()  # 每次创建新块后保存数据
        return block

    def new_transaction(self, **kwargs):
        """创建新交易，支持任意键值对"""
        self.current_transactions.append(kwargs)
        self.save_data()  # 每次添加新交易后保存数据
        return self.last_block["index"] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# 实例化区块链
blockchain = Blockchain()

# 实例化 Flask
app = Flask(__name__)


# 创建一个路由来显示整个区块链
@app.route("/chain", methods=["GET"])
def full_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain),
    }
    return jsonify(response), 200


# 创建一个路由来显示区块链的网页信息
@app.route("/chain/web", methods=["GET"])
def chain_web():
    # 将时间戳转换为可读格式
    formatted_chain = []
    for block in blockchain.chain:
        formatted_block = block.copy()
        formatted_block["timestamp"] = datetime.fromtimestamp(
            block["timestamp"]
        ).strftime("%Y-%m-%d %H:%M:%S")
        formatted_chain.append(formatted_block)

    # 使用模板显示区块链信息
    return render_template("chain.html", chain=formatted_chain)


# 创建一个路由来添加二维码识别记录
@app.route("/qrscan/new", methods=["POST"])
def new_qr_scan():
    values = request.get_json()

    # 检查 POST 请求中的字段是否完整
    required = ["qr_id", "scanner", "timestamp", "latitude", "longitude"]
    if not all(k in values for k in required):
        return "Missing values", 400

    # 创建新交易（二维码识别记录）
    index = blockchain.new_transaction(**values)
    response = {"message": f"QR scan record will be added to Block {index}"}
    return jsonify(response), 201


# 创建一个路由来挖矿
@app.route("/mine", methods=["GET"])
def mine():
    # 运行工作量证明算法来得到下一个证明值
    last_block = blockchain.last_block
    last_proof = last_block["proof"]
    proof = blockchain.proof_of_work(last_proof)

    # 必须在区块中记录一笔奖励交易
    blockchain.new_transaction(
        qr_id="0", scanner="system", timestamp=time(), latitude=0.0, longitude=0.0
    )

    # 创建新块并将其添加到区块链中
    block = blockchain.new_block(proof)

    response = {
        "message": "New Block Forged",
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
