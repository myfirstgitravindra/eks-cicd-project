from flask import Flask, jsonify, render_template_string
import os

app = Flask(__name__)

# CHANGE THIS VALUE TO V2, V3, ETC. TO VERIFY NEW DEPLOYMENTS!
APP_VERSION = "v1.0.0"

# HTML Template for a beautiful, modern landing page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EKS CI/CD Application</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            padding: 3rem;
            border-radius: 15px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        h1 { margin-bottom: 0.5rem; font-size: 2.5rem; }
        p { color: #e0e0e0; font-size: 1.1rem; }
        .badge {
            background-color: #4caf50;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 50px;
            font-weight: bold;
            display: inline-block;
            margin-top: 1rem;
            box-shadow: 0 4px 10px rgba(76, 175, 80, 0.3);
        }
        .pod-info {
            margin-top: 2rem;
            font-size: 0.85rem;
            color: #b0bec5;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Deployment Successful!</h1>
        <p>Your Jenkins to AWS EKS CI/CD pipeline is working flawlessly.</p>
        <div class="badge">Version: {{ version }}</div>
        <div class="pod-info">
            Served by Pod: {{ pod_name }}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    # Dynamically gets the Kubernetes Pod Name to show rolling updates in action
    pod_name = os.getenv('HOSTNAME', 'Local Environment')
    return render_template_string(HTML_TEMPLATE, version=APP_VERSION, pod_name=pod_name)

# CRUCIAL: Your EKS deployment.yaml probes point here!
@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "version": APP_VERSION
    }), 200

if __name__ == '__main__':
    # Runs on port 5000 as configured in your containerPort
    app.run(host='0.0.0.0', port=5000)

