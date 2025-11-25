import json
import re

import ollama
import pandas as pd

from datetime import datetime

class LLMInterface:
    def __init__(self):
        self.max_retries = 3
        self.base_prompt = """
        You are an expert software engineering assistant that classifies commit messages from a Git repository.  
        For each commit message, you will determine whether that commit message is a bug fix or not a bug fix. You can refer to the follow keywords to help identify bugs:  
        keywords = ['fix', 'bug', 'issue', 'error', 'problem', 'patch', 'crash', 'glitch', 'fault', 'defect'] 
        Consider intent and semantics, not just the keywords. 
        
        Return results in a JSON format as:  
        {'classification': 'bug fix | not bug fix', 'confidence': 0 – 1.0, 'explanation': 'explanation of your reasoning'} 
        
        Respond only with only valid JSON formatting.  
        Do not include additional information outside of the JSON results. 
        Classification must be exactly one of: bug fix, not bug fix.  
        Confidence must be a float value between 0 and 1.0  
        Explanation must be <= 30 words. 
        
        Example: 
        Message: 'Fix item clipping through wall when pressing forward on keyboard.' 
        Result: 
        {'classification': 'not bug fix', 'confidence': 1.0, 'explanation': 'commit message includes keywords relating to fix'} 
        
        Example: 
        Message: 'Add additional search options on home page. New options include expanded dropdown for searching by distance.’
        Result: 
        {'classification': 'bug fix', 'confidence': 1.0, 'explanation': ' commit message involves adding a new feature and does not relate to bug fixes'} 
        
        Commit Message: """

        self.model = 'llama3'
        self.role = 'user'


    def process_commits(self, commits):
        for commit in commits:

            #default/base values
            label = ''
            confidence = 0.0
            explanation = ''

            for i in range(self.max_retries):
                if i > 0:
                    print("Retrying due to invalid response.")

                response = self.prompt_llama(commit['message']).message.content
                # print(response)

                #troubleshooting response string to evaluate message format and handling of broken responses
                # response = ''''"classification": "not bug fix", "confidence": 1.0,
                #  "explanation": "commit message introduces a new file, which is not related to bug fixes"}'''


                #set empty string to account for instances of LLM not classifying
                if response is None:
                    response = ''

                #response should be loadable as a json
                try:
                    classification = json.loads(response)

                #if results don't load by default search for JSON format within the response instead
                except json.JSONDecodeError:
                    json_text = re.search(r'\{.*}', response, flags = re.S)
                    if not json_text:
                        classification = {}
                    else:
                        try:
                            classification = json.loads(json_text.group(0))
                        except json.JSONDecodeError:
                            classification = {}

                #if the LLM responses drops a non dict item then format it or provide empty dict to avoid crash
                if not isinstance(classification, dict):
                    if isinstance(classification, list):
                        if classification and isinstance(classification[0], dict):
                            classification = classification[0]
                    else:
                        classification = {}

                #use default values in instances where classification is inaccessible
                label_candidate = str(classification.get('classification', 'classification failed')).strip()

                if label_candidate in ('bug fix', 'not bug fix'):
                    label = label_candidate
                    confidence = classification.get('confidence')
                    explanation = classification.get('explanation')
                    break

                elif i == self.max_retries - 1 and label_candidate not in ('bug fix', 'not bug fix'):
                    label = 'not labeled'

            commit['classification'] = label
            commit['confidence'] = confidence
            commit['explanation'] = explanation
            print(commit['classification'], commit['confidence'], commit['explanation'])

        #export LLM analysis for troubleshooting purposes
        # now = datetime.now()
        # timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
        # df = pd.DataFrame(commits)
        # df.to_csv(f"LLM_results{timestamp}.csv", index = False)

        return commits

    def prompt_llama(self, commit):
        prompt = self.base_prompt + commit
        response = ollama.chat(model=self.model, messages=[{'role': self.role, 'content': prompt}])
        return response