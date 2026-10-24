import os
import sys
import socket
import platform
from datetime import datetime
from flask import Flask, render_template, jsonify, send_from_directory

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "container_id": socket.gethostname(),
        "student": "Hare Preeth (25BCE5652)",
        "platform": f"{platform.system()} ({platform.machine()})",
        "timestamp": datetime.utcnow().isoformat()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
