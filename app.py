from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# Create own credential file for development to use postgres DB
import postgres_credentials
import test_data

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
    id = db.Column(db.Integer, primary_key=True)
    affiliate_id = db.Column(db.Integer)
    paper_id = db.Column(db.Integer)

    def __init__(self, affiliate_id, paper_id):
        self.affiliate_id = affiliate_id
        self.paper_id = paper_id

class Link(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    name_1 = db.Column(db.String(200))
    name_2 = db.Column(db.String(200))
    count = db.Column(db.Integer)

    def __init__(self, name_1, name_2, count):
        self.name_1 = name_1
        self.name_2 = name_2
        self.count = count


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

class LinkSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name_1', 'name_2', 'count')

# Init schema
affiliates_schema = AffiliatesSchema(many=True)
paper_schema = PaperSchema(many=True)
author_schema = AuthorSchema(many=True)
link_schema = LinkSchema(many=True)


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
            affiliate = Affiliate(
                fullname=request.form["fullname"], 
                department=request.form["department"], 
                college=request.form["college"]
            )
            db.session.add(affiliate)
            db.session.commit()

        elif "paper" in request.form:
            paper = Paper(
                title=request.form["title"], 
                year=request.form["year"]
            )
            db.session.add(paper)
            db.session.commit()

            authors = request.form["authors"].split(",")
            if len(authors) > 1:
                for i in range(len(authors)):
                    for j in range(i + 1, len(authors)):
                        try:
                            link = db.session.query(Link).filter_by(name_1=authors[i], name_2=authors[j]).first()
                        except:
                            db.session.rollback()
                            try:
                                link = db.session.query(Link).filter_by(name_1=authors[j], name_2=authors[i]).first()
                            except:
                                db.session.rollback()
                                link = None

                        if link is None:
                            new_link = Link(
                                name_1=authors[i],
                                name_2=authors[j],
                                count=1
                            )
                            db.session.add(new_link)
                        else:
                            current_count = link.count
                            link.count = current_count + 1
                        db.session.commit()
    return render_template("new.html")

@app.route("/graph", methods=["GET"])
def get_graph():
    all_links = Link.query.all()
    result = link_schema.dump(all_links)
    nodes = set()
    for link in result:
        nodes.add(link["name_1"])
        nodes.add(link["name_2"])
    nodes = list(nodes)
    nodes = [{"id": node} for node in nodes]
    links = [{"source": link["name_1"], "target": link["name_2"], "value": link["count"]} for link in result]
    ret = {'nodes': nodes, 'links': links}
    if result != '':
        return jsonify(ret)

@app.route("/test", methods=["GET"])
def get_test():
    return jsonify(test_data.data)

if __name__ == "__main__":
    app.run()
