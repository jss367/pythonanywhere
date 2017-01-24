from flask import Flask, redirect, render_template, request, url_for
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="sappho$sapphodb",
    password="mysqldbpw0o0o",
    hostname="sappho.mysql.pythonanywhere-services.com",
    databasename="sappho$sapphodb",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

db = SQLAlchemy(app)

class Comment(db.Model):

    __tablename__ = "sapphodb"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))

class Feature(db.Model):

    __tablename__ = "sapphodb"

    id = db.Column(db.Integer, primary_key=True)
    feature_content = db.Column(db.String(4096))

comments = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html", comments=comments)

    comments.append(request.form["contents"])
    return redirect(url_for('index'))