from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, this is my LINE Bot!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render 會給你 PORT 環境變數
    app.run(host="0.0.0.0", port=port)