import pandas as pd

class StatisticsInterface:
    def __init__(self):
        pass

    def analyze_results(self, results):
        df = pd.DataFrame(results)


        aggregate_result = df.groupby('modified_files')
