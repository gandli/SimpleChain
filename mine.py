import requests


def mine_block():
    url = "http://127.0.0.1:5000/mine"
    response = requests.get(url)

    if response.status_code == 200:
        block_data = response.json()
        print("挖矿成功! 新区块已添加到区块链:")
        print(f"索引: {block_data['index']}")
        print(f"交易记录: {block_data['transactions']}")
        print(f"工作量证明: {block_data['proof']}")
        print(f"前一区块哈希值: {block_data['previous_hash']}")
    else:
        print(f"挖矿失败: {response.text}")


if __name__ == "__main__":
    mine_block()
