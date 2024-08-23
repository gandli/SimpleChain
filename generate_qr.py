from flask import Flask, render_template, send_file, request
import qrcode
from io import BytesIO

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    # 获取用户输入的数据
    data = request.form.get("qr_data")

    # 使用 qrcode 生成二维码
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    # 将生成的二维码保存到内存中
    img_io = BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
