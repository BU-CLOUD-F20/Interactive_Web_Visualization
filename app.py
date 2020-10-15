from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# Create own credential file for development to use postgres DB
import postgres_credentials

app = Flask(__name__)
CORS(app)

ENV = 'dev'

if ENV == 'dev':
    # Flask debug and Flask_SQLAlchemy connections
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = postgres_credentials.DATABASE_URI
else:
    app.debug = False
    app.config["SQLALCHEMY_DATABASE_URI"] = ""

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


# Affiliates class only used to create table within database
# To create new db in postgreSQL
# terminal >> python3
# >>> from app import db
# >>> db.create_all()
# DB should be created; exit()
class Affiliates(db.Model):
    __tablename__ = 'affiliates'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(200))
    department = db.Column(db.String(200))
    college = db.Column(db.String(200))

    def __init__(self, fullname, department, college):
        self.fullname = fullname
        self.department = department
        self.college = college


# Affiliate Schema used to for API retrieval
class AffiliatesSchema(ma.Schema):
    class Meta:
        fields = ('fullname', 'department', 'college')


# Init schema
affiliates_schema = AffiliatesSchema(many=True)


@app.route("/", methods=["GET"])
def get_affiliates():
    all_affiliates = Affiliates.query.all()
    result = affiliates_schema.dump(all_affiliates)
    if result != '':
        return jsonify(result)
        # return render_template("index.html", message="API GET is successful!")


if __name__ == "__main__":
    app.run()
