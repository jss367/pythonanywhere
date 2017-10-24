from flask import Flask, redirect, jsonify, render_template, request  # , url_for
from flask_sqlalchemy import SQLAlchemy
from text_analysis import analyze_text
import sys

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="sappho",
    password="mysqldbpw0o0o",
    hostname="sappho.mysql.pythonanywhere-services.com",
    databasename="sappho$comments",
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

db = SQLAlchemy(app)


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))


@app.route("/", methods=["GET", "POST"])
def index():
    errors = []
    results = {}
    verbs = {}
    if request.method == "POST":
        # comment = Comment(content=request.form["contents"])
        # db.session.add(comment)
        # db.session.commit()
        try:
            text = request.form['contents']
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
        # results = analyze_text(text)
        (results, verbs) = analyze_text(text)
    return render_template("main_page.html", errors=errors, results=results, verbs=verbs)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    print('The analyze() function in flask_app.py has been called', file=sys.stderr)
    errors = []

    mycontent = request.form.get('html', '')
    print('Here is the request form the analyze() function received by flask_app: \n{}'.format(mycontent), file=sys.stderr)
    try:
        text = request.form['contents']
    except:
        errors.append(
            "Unable to get URL. Please make sure it's valid and try again."
        )
    # Change this in between index and main page
    (results) = analyze_text(mycontent)
    # Change this in between index and main page
    print("Here is the response of the analyze function in flask_app:")
    print(repr(results), file=sys.stderr)
    return jsonify({'results': results})
