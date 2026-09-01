from flask import Flask
import socket

app = Flask(__name__)

@app.route("/")
def home():
    hostname = socket.gethostname()
    return f"Hello from EKS CI/CD Pipeline! Served by pod: {hostname}\n"

@app.route("/health")
def health():
    return "OK\n", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
