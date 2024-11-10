# app.py

from flask import Flask, jsonify
from books2scrape import scrape_data as scrape_books
from quotes2scrape import scrape_data as scrape_quotes
from jsonRest import fetch_json_data

app = Flask(__name__)
app.routes_printed = False


# Print all registered routes to ensure they are loaded
@app.before_request
def print_routes():
    if not app.routes_printed:
        print("Registered Routes:")
        for rule in app.url_map.iter_rules():
            print(rule)
        app.routes_printed = True


@app.route("/", methods=["GET"])
def index():
    print("Endpoint / called")
    return "Flask app is running"


@app.route("/scrape/books", methods=["GET"])
def get_books():
    print("Endpoint /scrape/books called")
    data = scrape_books()
    return jsonify(data)


@app.route("/scrape/quotes", methods=["GET"])
def get_quotes():
    print("Endpoint /scrape/quotes called")
    data = scrape_quotes()
    return jsonify(data)


@app.route("/fetch/json", methods=["GET"])
def get_json_data():
    print("Endpoint /fetch/json called")
    data = fetch_json_data()
    return jsonify(data)


@app.route("/routes", methods=["GET"])
def get_routes():
    print("Endpoint /routes called")
    return jsonify([str(rule) for rule in app.url_map.iter_rules()])


if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True, port=5001)
