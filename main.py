from flask import Flask, render_template, request, flash, get_flashed_messages, url_for
from flask_bootstrap import Bootstrap5

import os
from werkzeug.utils import redirect

from llm_interface import LLMInterface
from repository_interface import RepoInterface
from statisical_interface import StatisticsInterface
from Results import Results

#safety measure to minimize PyDriller errors during processing
os.environ['GIT_LFS_SKIP_SMUDGE'] = '1'

#initialize Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'

#initializ Bootstrap
Bootstrap5(app)

keywords = ['fix', 'bug', 'issue', 'error', 'problem', 'patch', 'crash', 'glitch', 'fault', 'defect']

#initialize repository interfacing
repository_interface = RepoInterface()

#initialize llm interfacing
llm_interface = LLMInterface()

#initialize llm interfacing
statistical_interface = StatisticsInterface()

resultList = list()

#TODO Home Route
@app.route('/')
def home():
    return render_template('index.html')

#TODO Selection Page
@app.route('/select', methods = ['GET', 'POST'])
def select_repo():
    if request.method == 'POST':
        # TODO - ideally validate REPO HERE if time permits
        repo_url = request.form.get('repository_url')
        print(f' Select_repo: {repo_url}')
        if repo_url is None:
            flash('The selected repository is not accessible. Please try again with another repository.')
            return redirect(url_for('select_repo'))
        else:
            print('It worked!')
            
            commits = repository_interface.retrieve_repository(repo_url)
            classification_results = llm_interface.process_commits(commits)
            statistical_results = statistical_interface.analyze_results(classification_results)
            
            result = Results(statistical_results["filename"].values[0], statistical_results["bug_density"].values[0])
            resultList.append(result)
            print(result.getFile() + " : " + result.getDensity())

            return redirect(url_for('show_results', repository_url=repo_url))
    return render_template('select_repo.html')

#TODO Results page
#TODO page should include info from statistics
@app.route('/results', methods = ['GET', 'POST'])
def show_results():
    return render_template('show_results.html', resultData=resultList)

if __name__ == '__main__':
    app.run(debug = True, port = 8080)