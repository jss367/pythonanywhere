from flask import Flask, redirect, jsonify, render_template, request#, url_for
from flask_sqlalchemy import SQLAlchemy
from text_analysis import analyze_text
from text_analysis2 import analyze_text2
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
        #db.session.commit()
        try:
            text = request.form['contents']
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
        #results = analyze_text(text)
        (results, verbs) = analyze_text(text)
    return render_template("main_page.html", errors=errors, results=results, verbs=verbs)

@app.route('/index', methods=['GET', 'POST'])
def new_index():
    errors = []
    results = {}

    verbs = {}
    text = "The text is not being found"
    if request.method == "POST":
        try:
            text = request.form['contents']
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
        (results, verbs) = analyze_text(text)
    return render_template('index.html', errors=errors, results=results, verbs=verbs)


@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == "POST":
        return("Jel")
    return render_template('post.html')



@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')




@app.route('/analyze', methods=['POST'])
def analyze():
    print('You made it to analyze', file=sys.stderr)
    errors = []
    results = {}

    verbs = {}
    mycontent = request.form.get('html', '')
    print('Here is the request form as received by flask_app: \n{}'.format(mycontent), file=sys.stderr)
    try:
        text = request.form['contents']
    except:
        errors.append(
            "Unable to get URL. Please make sure it's valid and try again."
        )
    #Change this in between index and main page
    (results, verbs) = analyze_text(mycontent)
    #Change this in between index and main page
    print(results, file=sys.stderr)
    return jsonify({'results': results, 'verbs': verbs})
