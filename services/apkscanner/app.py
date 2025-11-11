from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "apkscanner"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)

