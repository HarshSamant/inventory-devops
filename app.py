from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def connect_db():
    return sqlite3.connect("inventory.db")

@app.route("/add_item", methods=["POST"])
def add_item():
    data = request.get_json()
    name = data["name"]
    qty = data["qty"]

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name,qty) VALUES (?,?)", (name, qty))
    conn.commit()
    conn.close()

    return jsonify({"message": "Item added successfully!"})

@app.route("/list_items", methods=["GET"])
def list_items():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    return jsonify(items)

if __name__ == "__main__":
    conn = connect_db()
    conn.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, qty INTEGER)")
    conn.close()
    app.run(debug=True)

