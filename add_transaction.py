import requests
import json


def add_transaction(
    qr_id, scanner, timestamp, latitude, longitude, additional_data=None
):
    url = "http://127.0.0.1:5000/qrscan/new"
    transaction_data = {
        "qr_id": qr_id,
        "scanner": scanner,
        "timestamp": timestamp,
        "latitude": latitude,
        "longitude": longitude,
    }

    # 如果有额外的数据（如可扩展字段），则添加到请求中
    if additional_data:
        transaction_data.update(additional_data)

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(transaction_data), headers=headers)

    if response.status_code == 201:
        print("交易成功添加到区块链!")
    else:
        print(f"添加交易失败: {response.text}")


if __name__ == "__main__":
    # 示例数据，实际场景中可以从输入或其他来源获取
    qr_id = "12345"
    scanner = "user1"
    timestamp = 1724372101.8020952
    latitude = 37.7749
    longitude = -122.4194

    # 额外的数据可以通过字典形式传入（可选）
    additional_data = {
        "custom_field_1": "example_value_1",
        "custom_field_2": "example_value_2",
    }

    # 添加交易
    add_transaction(qr_id, scanner, timestamp, latitude, longitude, additional_data)
