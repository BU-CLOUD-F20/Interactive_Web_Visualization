from flask import Flask
from app import api_bp
from flask_cors import CORS
from algorithms.parsescival import parse_scival as ps
import os, time

def load_data():
    current_path = os.path.dirname((os.path.realpath(__file__)))
    sheet_path = current_path + '/' + 'scivalsheets/'
    preset = []
    for filename in os.listdir(sheet_path):
        preset += (ps().getXLS(os.path.join(sheet_path, filename)))

    print(preset)

def create_app():
    app = Flask(__name__)

    app.register_blueprint(api_bp, url_prefix="/api")

    CORS(app)

    return app

if __name__ == "__main__":
    load_data()
    app = create_app()
    app.run(debug=True, port=8080, host='0.0.0.0')