from flask import Flask, jsonify, render_template_string
import os
import logging
from splunk_handler import SplunkHandler

app = Flask(__name__)
APP_VERSION = "v1.0.0"

# ----------------------------------------------------------------
# LIVE SPLUNK CONFIGURATION
# ----------------------------------------------------------------
splunk_logger = SplunkHandler(
    host='32.192.216.174',
    port=8088,
    token='c2ecf9fe-6a30-4cd2-9ae0-1e38a1c2f863',
    index='main',
    verify=False
)

logger = logging.getLogger('eks_app')
logger.setLevel(logging.INFO)
logger.addHandler(splunk_logger)
# ----------------------------------------------------------------

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head><title>EKS App</title></head>
<body style="background:#1e3c72; color:white; text-align:center; padding:50px;">
    <h1>🚀 Deployment Successful!</h1>
    <p>Version: {{ version }}</p>
</body>
</html>
"""

@app.route('/')
def home():
    pod_name = os.getenv('HOSTNAME', 'Local Environment')
    logger.info(f"Homepage accessed by pod: {pod_name}")
    return render_template_string(HTML_TEMPLATE, version=APP_VERSION)

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "version": APP_VERSION}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
