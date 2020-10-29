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
class Affiliate(db.Model):
    __tablename__ = 'affiliates'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(200))
    department = db.Column(db.String(200))
    college = db.Column(db.String(200))

    def __init__(self, fullname, department, college):
        self.fullname = fullname
        self.department = department
        self.college = college

class Paper(db.Model):
    __tablename__ = 'papers'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    year = db.Column(db.Integer)

    def __init__(self, title, year):
        self.title = title
        self.year = year

class Author(db.Model):
    __tablename__ = 'authors'
    affiliate_id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, primary_key=True)

class Link(db.Model):
    __tablename__ = 'links'
    id_1 = db.Column(db.Integer, primary_key=True)
    id_2 = db.Column(db.Integer, primary_kay=True)


# Affiliate Schema used to for API retrieval
class AffiliatesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'fullname', 'department', 'college')

class PaperSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'year')

class AuthorSchema(ma.Schema):
    class Meta:
        fields = ('affiliate_id', 'paper_id')

# Init schema
affiliates_schema = AffiliatesSchema(many=True)
paper_schema = PaperSchema(many=True)
author_schema = AuthorSchema(many=True)


@app.route("/", methods=["GET"])
def get_affiliates():
    all_affiliates = Affiliate.query.all()
    result = affiliates_schema.dump(all_affiliates)
    if result != '':
        return jsonify(result)
        # return render_template("index.html", message="API GET is successful!")

@app.route("/new", methods=["GET", "POST"])
def new_entity():
    if request.method == "POST":
        if "affiliate" in request.form:
            print("affiliate")
            affiliate = Affiliate(
                fullname=request.form["fullname"], 
                department=request.form["department"], 
                college=request.form["college"])
            db.session.add(affiliate)
            db.session.commit()
        elif "paper" in request.form:
            print("paper")
            paper = Affiliate(
                title=request.form["title"], 
                year=request.form["year"])
            db.session.add(paper)
            authors = request.form["authors"].split(",")
            if len(authors > 1):
                for author in request.form["authors"].split(","):
                    pass
            db.session.commit()
        # affiliate = Affiliate(fullname="")
    return render_template("new.html") 

if __name__ == "__main__":
    app.run()
