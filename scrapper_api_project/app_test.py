from flask import Flask, jsonify

app = Flask(__name__)


# Test Route
@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Flask is working!"})


if __name__ == "__main__":
    app.run(debug=True)
