import pandas as pd


class StatisticsInterface:
    def __init__(self):
        pass

    def analyze_results(self, results):
        df = pd.DataFrame(results)

        # expand the modified files field to
        df = df.explode('modified_files', ignore_index=True)

        # convert modfiles into files, deletions, insertions at file level
        df['filename'] = df['modified_files'].apply(lambda d: d['path'] if isinstance(d, dict) else None)
        df['file_added'] = df['modified_files'].apply(lambda d: d['added_lines'] if isinstance(d, dict) else 0)
        df['file_deleted'] = df['modified_files'].apply(lambda d: d['deleted_lines'] if isinstance(d, dict) else 0)

        df = df.drop(columns=['modified_files'])

        df['classification'] = df['classification'].astype(str).str.strip().str.lower()
        df['is_bug_fix'] = df['classification'].eq('bug fix').astype(int)
        df['is_not_labeled'] = df['classification'].eq('not labeled').astype(int)

        # help ensure filename matching by formatting the names
        filename_series = df['filename'].fillna('').astype(str).str.strip().str.lower()

        # isolate file extensions to assist with matching
        df['ext'] = filename_series.str.extract(r'(\.[^.\\]+(?:\.[^.\\]+)*)$', expand=False)

        keep_extensions = ('.py', '.java', '.class', '.jar', '.c', '.cpp', '.h', '.hpp', '.hxx', '.html', '.htm',
                           '.css', '.js', '.php', '.cs', '.swift', '.vb', '.sh', '.pl', '.go', '.rb')

        keep_mask = df['ext'].isin(keep_extensions)
        df.loc[~keep_mask, 'is_bug_fix'] = 0


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

        # health metric to monitor how many LLM classifications were unsuccessful
        aggregate_result['failed_classification_density'] = (
                    aggregate_result['is_not_labeled'] / aggregate_result['commit_count'])

        aggregate_result = aggregate_result.sort_values('bug_density', ascending=False)
        aggregate_result = aggregate_result.reset_index()

        aggregate_result.to_csv('output.csv', index=False)

        return aggregate_result
