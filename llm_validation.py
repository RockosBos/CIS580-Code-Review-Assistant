import pandas as pd
from llm_interface import LLMInterface

# #method to evaluate validation_data - uncomment to rerun full process on the csv
# #initialize llm interfacing
# llm_interface = LLMInterface()
#
# validation_df = pd.read_csv('data/validation_data.csv')
#
# #llm interface expects a dictionary
# commits = validation_df.to_dict(orient = 'records')
#
# classification_results = llm_interface.process_commits(commits)
#
# validation_with_llm = pd.DataFrame(classification_results)
# validation_with_llm.to_csv('data/validation_data_with_llm_labels.csv', index = False)

#load existing results
results_df = pd.read_csv('data/validation_data_with_llm_labels.csv')
llm_label_accuracy = (results_df['classification'] == results_df['manual label']).mean() * 100.00

print("LLM Accuracy in Classifying Bug Fixes", round(llm_label_accuracy,2))