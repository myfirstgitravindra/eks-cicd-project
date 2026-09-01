from flask import Flask
import socket
import platform
from datetime import datetime

app = Flask(__name__)

APP_VERSION = "v3"

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>EKS CI/CD Pipeline</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Segoe UI', Roboto, Arial, sans-serif;
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #fff;
  }}
  .card {{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 20px;
    padding: 48px 56px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    max-width: 480px;
  }}
  .badge {{
    display: inline-block;
    background: #00e676;
    color: #063;
    font-weight: 700;
    font-size: 13px;
    padding: 4px 14px;
    border-radius: 999px;
    margin-bottom: 18px;
    letter-spacing: 0.5px;
  }}
  h1 {{
    font-size: 28px;
    margin-bottom: 10px;
    background: linear-gradient(90deg, #00e676, #00b0ff);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }}
  p {{
    font-size: 15px;
    color: #cfd8dc;
    margin: 6px 0;
  }}
  .meta {{
    margin-top: 24px;
    padding-top: 20px;
    border-top: 1px solid rgba(255,255,255,0.15);
    font-size: 13px;
    color: #90a4ae;
    text-align: left;
  }}
  .meta span {{ color: #00e676; font-weight: 600; }}
  .pulse {{
    width: 10px; height: 10px;
    background: #00e676;
    border-radius: 50%;
    display: inline-block;
    margin-right: 8px;
    box-shadow: 0 0 0 rgba(0,230,118,0.6);
    animation: pulse 1.5s infinite;
  }}
  @keyframes pulse {{
    0% {{ box-shadow: 0 0 0 0 rgba(0,230,118,0.6); }}
    70% {{ box-shadow: 0 0 0 10px rgba(0,230,118,0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(0,230,118,0); }}
  }}
</style>
</head>
<body>
  <div class="card">
    <div class="badge">VERSION {version}</div>
    <h1>🚀 EKS CI/CD Pipeline</h1>
    <p><span class="pulse"></span>Live and running on Kubernetes</p>
    <p>Deployed automatically via Jenkins + GitHub Webhook</p>
    <div class="meta">
      <p>Pod: <span>{hostname}</span></p>
      <p>Platform: <span>{platform}</span></p>
      <p>Server time: <span>{time}</span></p>
    </div>
  </div>
</body>
</html>
"""

@app.route("/")
def home():
    hostname = socket.gethostname()
    return PAGE.format(
        version=APP_VERSION,
        hostname=hostname,
        platform=platform.platform(),
        time=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
    )

@app.route("/health")
def health():
    return "OK\n", 200

@app.route("/version")
def version():
    return f"{APP_VERSION}\n", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
