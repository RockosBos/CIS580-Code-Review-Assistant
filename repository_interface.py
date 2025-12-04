import git.exc
import pydriller


class RepoInterface:
    def __init__(self):
        pass

        # TODO (time permitting)

    def validate_url(self, repository_url):
        pass

    def retrieve_repository(self, repository_url):
        commits = []
        print(f'Retrieve repo: {repository_url}')
        try:
            for commit in pydriller.Repository(path_to_repo=repository_url).traverse_commits():

                #file names were not being tracked consistently so compile as separate list and then append
                #initial deletions and insertions were commit-level and need to be saved at file level too
                mod_files = []

                for modfile in commit.modified_files:
                    path = modfile.new_path or modfile.old_path or modfile.filename
                    mod_files.append({
                        'path': path,
                        'added_lines': modfile.added_lines,
                        'deleted_lines': modfile.deleted_lines})


                commits.append({
                    'hash': commit.hash,
                    'message': commit.msg,
                    'date': commit.committer_date,
                    'modified_files': mod_files,
                    'parents': commit.parents,
                    'files': commit.files,
                    'lines': commit.lines})

            return commits
        except git.exc.GitCommandError:
            print('Repository not accessible.')
            return commits
