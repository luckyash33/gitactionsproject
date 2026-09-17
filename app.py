# Aviz Academy - Batch 8 | DevSecOps Training
# Sample Flask app to demonstrate Docker + GitHub Actions CI pipeline
# "Learn by Doing, Not Just Watching" - avizacademy.com

from flask import Flask, jsonify
import platform
import os
import datetime

app = Flask(__name__)

START_TIME = datetime.datetime.utcnow()


def uptime():
    delta = datetime.datetime.utcnow() - START_TIME
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"


@app.route("/")
def home():
    return jsonify({
        "app": "Aviz Academy - GitHub Actions Demo",
        "batch": "Batch 7 GHA Topic - DevSecOps",
        "message": "Learn by Doing, Not Just Watching!",
        "website": "avizacademy.com",
        "status": "running"
    })


@app.route("/health")
def health():
    """Health check endpoint — used by Docker and load balancers"""
    return jsonify({
        "status": "This app is healthy",
        "uptime": uptime(),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }), 200


@app.route("/info")
def info():
    """System info — great for verifying what's inside the container"""
    return jsonify({
        "python_version": platform.python_version(),
        "os": platform.system(),
        "hostname": platform.node(),
        "environment": os.getenv("APP_ENV", "development"),
        "port": os.getenv("PORT", "5000"),
        "built_by": "Aviz Academy CI Pipeline"
    })


@app.route("/topics")
def topics():
    """What Batch 8 is learning"""
    return jsonify({
        "batch": "Batch 7",
        "track": "DevSecOps",
        "topics_covered": [
            "Docker fundamentals",
            "GitHub Actions CI/CD",
            "Reusable workflows",
            "Docker image scanning with Trivy",
            "Shift-left security",
            "Kubernetes deployments",
            "Terraform IaC",
            "AWS cloud services"
        ],
        "current_session": "Docker Build + Scan pipeline"
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=False)
