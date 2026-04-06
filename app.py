from flask import Flask, request, jsonify
import db

app = Flask(__name__)

@app.route('/ranking', methods=['GET'])
def ranking():


if __name__ == '__main__':
    app.run(port=5000, debug=True)

