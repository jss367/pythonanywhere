from flask import Flask, redirect, render_template, request, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from text_analysis import analyze_text
from text_analysis2 import analyze_text2

import re
import nltk
from stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup

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
    if request.method == "POST":
        #comment = Comment(content=request.form["contents"])
        #db.session.add(comment)
        #db.session.commit()
        try:
            text = request.form['contents']
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
        results = analyze_text(text)
    return render_template("main_page.html", errors=errors, results=results)
        #return render_template("main_page.html", comments=Comment.query.all(), errors=errors, results=results)
        #return redirect(url_for('index'))


@app.route('/index', methods=['GET', 'POST'])
def new_index():
    errors = []
    results = {}
    if request.method == "POST":
        try:
            text = request.form['contents']
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
        results = analyze_text2(text)
        #raw = Comment(content=request.form["contents"])
        #nltk.data.path.append('./nltk_data/')  # set the path
        #tokens = nltk.word_tokenize(raw)
        #text = nltk.Text(tokens)
        # save the results
        #results = sorted(
        #    raw_word_count.items(),
        #    reverse=True
        #   )
    #    try:
    #        result = Result(
    #            url=url,
    #            result_all=raw_word_count,
    #            result_no_stop_words=no_stop_words_count
    #            )
    #        db.session.add(result)
    #       db.session.commit()
    #   except:
    #        errors.append("Unable to add item to database.")
    return render_template('index.html', errors=errors, results=results)


@app.route('/post')
def post():
    return render_template('post.html')