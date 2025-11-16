import git.exc
import pydriller


class RepoInterface:
    def __init__(self):
        pass

        # TODO (time permitting)

    def validate_url(self, repository_url):
        pass

    def retrieve_repository(self, repository_url):
        # TODO 
        commits = []
        print(f'Retrieve repo: {repository_url}')
        try:
            for commit in pydriller.Repository(path_to_repo=repository_url).traverse_commits():
                commits.append({
                    'hash': commit.hash,
                    'message': commit.msg,
                    'date': commit.committer_date,
                    'modified_files': [modfile.filename for modfile in commit.modified_files],
                    'parents': commit.parents,
                    'files': commit.files,
                    'lines': commit.lines,
                    'deletions': commit.deletions,
                    'insertions': commit.insertions})
            return commits
        except git.exc.GitCommandError:
            print('Repository not accessible.')
            return commits
