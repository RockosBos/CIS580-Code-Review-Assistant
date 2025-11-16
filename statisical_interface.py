import os.path

import pandas as pd

class StatisticsInterface:
    def __init__(self):
        pass

    def analyze_results(self, results):
        df = pd.DataFrame(results)

        #expand the modified files field to
        df = df.explode('modified_files', ignore_index = True)
        df = df.rename(columns ={'modified_files': 'filename'})

        df['is_bug_fix'] = df['classification'].eq('bug fix').astype(int)

        # non-code files are being flagged as bug fixes due to the commit messages - exclude these files by setting is_bug_fix = 0
        drop_extensions = ('.gitignore', '.suo', '.backup', '.png', '.jpg', '.jpeg', '.meta', '.settings',
                           '.prefab', '.unity', '.wav', '.asset', '.fbx')

        filename_series = df['filename'].astype(str).str.lower()
        drop_mask = filename_series.str.endswith(drop_extensions, na = False)
        df.loc[drop_mask, 'is_bug_fix'] = 0

        aggregate_result = df.groupby('filename', as_index=False).agg({
            'hash': 'count',
            'lines': 'sum',
            'deletions': 'sum',
            'insertions': 'sum',
            'is_bug_fix': 'sum',
        }).rename(columns={'hash': 'commit_count',
                           'is_bug_fix': 'bug_fix_commits'})

        aggregate_result['bug_density'] = (aggregate_result['bug_fix_commits'] / aggregate_result['commit_count'])

        aggregate_result = aggregate_result.sort_values('bug_density', ascending = False)
        aggregate_result = aggregate_result.reset_index()

        aggregate_result.to_csv('output.csv', index = False)

        return aggregate_result