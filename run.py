from flask import Flask
from app import api_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    app.register_blueprint(api_bp, url_prefix="/api")

    CORS(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8080, host='0.0.0.0')