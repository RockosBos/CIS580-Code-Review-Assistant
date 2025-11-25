import pandas as pd

class StatisticsInterface:
    def __init__(self):
        pass

    def analyze_results(self, results):
        df = pd.DataFrame(results)

        #expand the modified files field to
        df = df.explode('modified_files', ignore_index = True)

        #convert modfiles into files, deletions, insertions at file level
        df['filename'] = df['modified_files'].apply(lambda d: d['path'] if isinstance(d, dict) else None)
        df['file_added'] = df['modified_files'].apply(lambda d: d['added_lines'] if isinstance(d, dict) else 0)
        df['file_deleted'] = df['modified_files'].apply(lambda d: d['deleted_lines'] if isinstance(d, dict) else 0)

        df = df.drop(columns = ['modified_files'])

        df['classification'] = df['classification'].astype(str).str.strip().str.lower()
        df['is_bug_fix'] = df['classification'].eq('bug fix').astype(int)
        df['is_not_labeled'] = df['classification'].eq('not labeled').astype(int)

        # non-code files are being flagged as bug fixes due to the commit messages - exclude these files by setting is_bug_fix = 0
        drop_extensions = ('.gitignore', '.suo', '.backup', '.png', '.jpg', '.jpeg', '.meta', '.settings',
                           '.prefab', '.unity', '.wav', '.asset', '.fbx', '.bin', '.zip', '.pak',
                           '.dll', '.exe', '.tiff', '.tif', '.mp4', '.mp3', '.mov', '.info')

        filename_series = df['filename'].astype(str).str.lower()
        drop_mask = filename_series.str.endswith(drop_extensions, na = False)
        df.loc[drop_mask, 'is_bug_fix'] = 0

        aggregate_result = df.groupby('filename', as_index=False).agg({
            'hash': 'count',
            'date': 'max',
            'lines': 'sum',
            'file_deleted': 'sum',
            'file_added': 'sum',
            'is_bug_fix': 'sum',
            'is_not_labeled': 'sum'
        }).rename(columns={'hash': 'commit_count',
                           'is_bug_fix': 'bug_fix_commits',
                           'date': 'last_commit_date'
                           })

        aggregate_result = aggregate_result[aggregate_result['commit_count'] > 1]

        aggregate_result['bug_density'] = (aggregate_result['bug_fix_commits'] / aggregate_result['commit_count'])

        #health metric to monitor how many LLM classifications were unsuccessful
        aggregate_result['failed_classification_density'] = (aggregate_result['is_not_labeled'] / aggregate_result['commit_count'])

        aggregate_result = aggregate_result.sort_values('bug_density', ascending = False)
        aggregate_result = aggregate_result.reset_index()

        aggregate_result.to_csv('output.csv', index = False)

        return aggregate_result