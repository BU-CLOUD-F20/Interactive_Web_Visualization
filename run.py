from flask import Flask, jsonify
from flask_cors import CORS
from algorithms.parsescival import parse_scival as ps
import os, time
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import create_engine, Table, Column, MetaData, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
CORS(app)

def load_api():
    from app import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

if __name__ == "__main__":
    # app = create_app()
    # affiliates_schema = load_item()
    # load_item()
    load_api()
    app.run(debug=True, port=8080, host='0.0.0.0')