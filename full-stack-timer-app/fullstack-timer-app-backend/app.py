from flask import Flask, jsonify
# import psycopg2


records_list = [
    {"color": "red", "food": "apple"},
    {"color": "blue", "food": "blueberry"}
]

app = Flask(__name__)

@app.route("/records")
def records_get_all():
    return jsonify({"message": "records found", "results": records_list})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port='8086')
