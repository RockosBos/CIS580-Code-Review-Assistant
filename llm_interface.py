import json
import re

import ollama

class LLMInterface:
    def __init__(self):
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
            response = self.prompt_llama(commit['message']).message.content
            # print(response)

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
            if not isinstance(classification, dict):
                classification = {}

            #use default values in instances where classification is inaccessible
            label = str(classification.get('classification', 'not_labeled')).strip()
            confidence = classification.get('confidence', 0.0)
            explanation = classification.get('explanation', '')

            commit['classification'] = label
            commit['confidence'] = confidence
            commit['explanation'] = explanation
            print(commit['classification'], commit['confidence'], commit['explanation'])

        return commits

    def prompt_llama(self, commit):
        prompt = self.base_prompt + commit
        response = ollama.chat(model=self.model, messages=[{'role': self.role, 'content': prompt}])
        return response