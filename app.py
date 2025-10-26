from datetime import datetime

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/our_story")
def our_story():
    with open("static/images/our-story/captions.txt", "r", encoding="utf-8") as file:
        captions = [line.strip() for line in file.readlines()]
    return render_template("our_story.html", captions=captions)


@app.route("/schedule")
def schedule():
    return render_template("schedule.html")


@app.route("/travel")
def travel():
    return render_template("travel.html")


@app.route("/faq")
def faq():
    return render_template("faq.html")


if __name__ == "__main__":
    app.run(debug=True)
