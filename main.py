from flask import Flask, render_template, jsonify, request
import requests
import os

app = Flask(__name__)

API_PIMA = os.environ.get("API_PIMA_URL", "https://apiparagit.onrender.com/precios")

# Middleware para mostrar la IP en logs
@app.before_request
def log_ip():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    print(f"[LOG] Conexión desde IP: {ip} - Endpoint: {request.path}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/precios")
def precios():
    try:
        res = requests.get(API_PIMA, timeout=10)
        res.raise_for_status()
        return jsonify(res.json())
    except Exception as e:
        print(f"[ERROR] No se pudo obtener datos de PIMA: {e}")
        return jsonify({"error": f"No se pudo obtener datos de PIMA: {e}"}), 500

@app.route("/pima")
def pima():
    return render_template("pima.html")



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
