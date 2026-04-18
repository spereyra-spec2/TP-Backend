from flask import Flask
from flask_cors import CORS
from routes.ranking import ranking_bp


app = Flask(__name__)
CORS(app)

@app.register_blueprint(ranking_bp, url_prefix="/ranking")


if __name__ == "__main__":
    app.run(port=5000,debug=True)

