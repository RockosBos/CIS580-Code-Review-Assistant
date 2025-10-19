from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

#initialize Flask App
app = Flask(__name__)

#initializ Bootstrap
Bootstrap5(app)

#TODO Home Route
@app.route("/")
def home():
    return render_template("index.html")

#TODO Selection Page
@app.route("/select")
def select_repo():
    return render_template("select_repo.html")

#TODO Results page
@app.route("/results")
def show_results():
    pass


if __name__ == "__main__":
    app.run(debug = True, port = 8080)