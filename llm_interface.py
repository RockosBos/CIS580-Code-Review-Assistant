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
            commit['classification'] = self.prompt_llama(commit['message'])


    def prompt_llama(self, commit):
        prompt = self.base_prompt + commit
        response = ollama.chat(model=self.model, messages=[{'role': self.role, 'content': prompt}])
        #print(response, "\n")
        return response