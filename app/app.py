from flask import Flask, render_template
from form import Form

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

@app.route("/")
def form():
	form = Form()
	return render_template('form.html', title='Form', form=form)
