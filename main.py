from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
import pydriller
import os

#safety measure to minimize PyDriller errors during processing
os.environ['GIT_LFS_SKIP_SMUDGE'] = '1'

#initialize Flask App
app = Flask(__name__)

#initializ Bootstrap
Bootstrap5(app)

#TODO Home Route
@app.route('/')
def home():
    return render_template('index.html')

#TODO Selection Page
@app.route('/select')
def select_repo():
    return render_template('select_repo.html')

#TODO Results page
@app.route('/results', methods = ['GET', 'POST'])
def show_results():
    repository_url = None
    # print(request.method)
    if request.method == 'POST':
        repository_url = request.form.get('repository_url')
        print(repository_url)
    return render_template('show_results.html', repository_url = repository_url)

# 'C:/Users/Owner/PycharmProjects/CIS580-Code-Review-Assistant'

if __name__ == '__main__':
    app.run(debug = True, port = 8080)