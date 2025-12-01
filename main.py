from flask import Flask, render_template, request, flash, get_flashed_messages, url_for, make_response
from flask_bootstrap import Bootstrap5

import os
from werkzeug.utils import redirect

from llm_interface import LLMInterface
from repository_interface import RepoInterface
from statisical_interface import StatisticsInterface
from Results import Results

import csv
import operator
from io import StringIO

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

result_list = list()
density_list = list()
ts_list = list()
filtered_density_list = list()
filtered_ts_list = list()
most_buggy_files = list()

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
			
			result_list.clear()
			for i in statistical_results.itertuples(index=False):
				result = Results(i.filename, i.bug_density, i.last_commit_date)
				result_list.append(result)

			return redirect(url_for('show_results', repository_url=repo_url))
	return render_template('select_repo.html')

#TODO Results page
#TODO page should include info from statistics
@app.route('/results', methods = ['GET', 'POST'])
def show_results():
	if request.method == "POST":
		if 'genCSVButton' in request.form:
			with open('results.csv', 'w', newline='') as f:
				field_names = ["File", "Bug Density", "Last Commit Date"]
				writer = csv.DictWriter(f, fieldnames=field_names)
				writer.writeheader()
				for i in result_list:
					writer.writerow({"File": i.getFile(), "Bug Density": i.getDensity(), "Last Commit Date":i.getLastCommitDate()})
			return render_template('show_results.html', resultData=result_list, tsData=ts_list)
		if 'ReturnToRepoSelectButton' in request.form:
			return render_template('select_repo.html')
	else:        
		ts_list = sorted(result_list, key=operator.attrgetter('lastEdit'), reverse=True)
		filtered_ts_list = [f for f in ts_list if (f.getDensity() != "0.0")]
		ts_list.clear()
		iter = 0
		for i in filtered_ts_list:
			if iter < 5:
				ts_list.append(i)
				iter = iter + 1
			else:
				break

		most_buggy_files = [f for f in result_list if float(f.getDensity()) > 0.25]
		top_density_results = sorted(most_buggy_files, key=lambda f: float(f.getDensity()), reverse = True)

	for i in ts_list:
		print(i.getFile(), i.getDensity())

	return render_template('show_results.html', resultData=result_list, tsData=ts_list, top_density_results = top_density_results)

if __name__ == '__main__':
	app.run(debug = True, port = 8080)