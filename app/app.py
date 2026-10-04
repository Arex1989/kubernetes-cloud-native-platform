import os
import socket
from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "cloud-native-platform-api")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

REQUEST_COUNT = Counter(
    "platform_api_requests_total",
    "Total number of requests received by the platform API",
    ["endpoint"],
)


@app.route("/")
def index():
    REQUEST_COUNT.labels(endpoint="/").inc()

    return jsonify(
        {
            "application": APP_NAME,
            "version": APP_VERSION,
            "environment": ENVIRONMENT,
            "hostname": socket.gethostname(),
            "status": "running",
        }
    )


@app.route("/health")
def health():
    REQUEST_COUNT.labels(endpoint="/health").inc()

    return jsonify(
        {
            "status": "healthy",
            "application": APP_NAME,
        }
    )


@app.route("/ready")
def ready():
    REQUEST_COUNT.labels(endpoint="/ready").inc()

    return jsonify(
        {
            "status": "ready",
            "application": APP_NAME,
        }
    )


@app.route("/version")
def version():
    REQUEST_COUNT.labels(endpoint="/version").inc()

    return jsonify(
        {
            "application": APP_NAME,
            "version": APP_VERSION,
        }
    )


@app.route("/metrics")
def metrics():
    REQUEST_COUNT.labels(endpoint="/metrics").inc()
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
