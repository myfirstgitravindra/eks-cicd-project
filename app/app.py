from flask import Flask
import socket
 
app = Flask(__name__)
 
APP_VERSION = "v2"
 
@app.route("/")
def home():
    hostname = socket.gethostname()
    return f"Hello from EKS CI/CD Pipeline! Version {APP_VERSION} served by pod: {hostname}\n"
 
@app.route("/health")
def health():
    return "OK\n", 200
 
@app.route("/version")
def version():
    return f"{APP_VERSION}\n", 200
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
