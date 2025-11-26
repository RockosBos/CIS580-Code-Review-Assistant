from flask import Flask, render_template, request, flash, get_flashed_messages, url_for
from flask_bootstrap import Bootstrap5

import os
from werkzeug.utils import redirect

from llm_interface import LLMInterface
from repository_interface import RepoInterface
from statisical_interface import StatisticsInterface
from Results import Results

import csv
import operator

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
densityList = list()
TSList = list()
filteredDensityList = list()
filteredTSList = list()

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
			
			resultList.clear()
			for i in statistical_results.itertuples(index=False):
				result = Results(i.filename, i.bug_density, i.last_commit_date)
				resultList.append(result)

			return redirect(url_for('show_results', repository_url=repo_url))
	return render_template('select_repo.html')

#TODO Results page
#TODO page should include info from statistics
@app.route('/results', methods = ['GET', 'POST'])
def show_results():
	if request.method == "POST":
		if 'genCSVButton' in request.form:
			with open('results.csv', 'w', newline='') as f:
				fieldNames = ["File", "Bug Density", "Last Commit Date"]
				writer = csv.DictWriter(f, fieldnames=fieldNames)
				writer.writeheader()
				for i in resultList:
					writer.writerow({"File": i.getFile(), "Bug Density": i.getDensity(), "Last Commit Date":i.getLastCommitDate()})
			return render_template('show_results.html', resultData=resultList, tsData=TSList)
		if 'ReturnToRepoSelectButton' in request.form:
			return render_template('select_repo.html')
	else:        
		TSList = sorted(resultList, key=operator.attrgetter('lastEdit'), reverse=True)
		filteredTSList = [f for f in TSList if (f.getDensity() != "0.0")]
		TSList.clear()
		iter = 0
		for i in filteredTSList:
			if(iter < 5):
				TSList.append(i)
				iter = iter + 1
			else:
				break
	for i in TSList:
		print(i.getFile(), i.getDensity())
	return render_template('show_results.html', resultData=resultList, tsData=TSList)

if __name__ == '__main__':
	app.run(debug = True, port = 8080)