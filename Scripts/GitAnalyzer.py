# We need PyDriller to pull git repository information
from pydriller import Repository

# Pandas is a nice utility and here it allows us to write to CSVs easily
import pandas as pd

def sanitize_message(msg):
    """
    Removes newlines from commit messages and returns the cleansed message
    """
    msg = msg.replace('\r\n', ' ')
    msg = msg.replace('\n', ' ')
    msg = msg.replace(',', '')
    msg = msg.replace('"', '')
    return msg

def build_commits(repo):
    """
    Builds a list of commit objects for a repository
    """
    commits = []
    for commit in repo.traverse_commits():

        hash = commit.hash
        try:

            # Gather a list of files modified in the commit
            files = []
            for f in commit.modified_files:
                if f.new_path is not None:
                    files.append(f.new_path) 

            # Sanitize the message to prevent it from confusing our resulting CSV
            msg = sanitize_message(commit.msg)

            # Optimization to prevent requesting same data twice
            author = commit.author
            committer = commit.committer
            inserts = commit.insertions
            deletions = commit.deletions

            # Capture information about the commit in object format so I can reference it later
            record = {
                'hash': hash,
                'message': msg,
                'author_name': author.name,
                'author_email': author.email,
                'author_date': commit.author_date,
                'author_tz': commit.author_timezone,
                'committer_name': committer.name,
                'committer_email': committer.email,
                'committer_date': commit.committer_date,
                'committer_tz': commit.committer_timezone,
                'in_main': commit.in_main_branch,
                'is_merge': commit.merge,
                'num_deletes': deletions,
                'num_inserts': inserts,
                'net_lines': inserts - deletions,
                'num_files': commit.files,
                'branches': ', '.join(commit.branches), # Comma separated list of branches the commit is found in
                'files': ', '.join(files), # Comma separated list of files the commit modifies
                'pydriller_files': commit.modified_files,
                # PyDriller Open Source Delta Maintainability Model (OS-DMM) stat. See https://pydriller.readthedocs.io/en/latest/deltamaintainability.html for metric definitions
                'dmm_unit_size': commit.dmm_unit_size,
                'dmm_unit_complexity': commit.dmm_unit_complexity,
                'dmm_unit_interfacing': commit.dmm_unit_interfacing,
            }
            # Omitted: modified_files (list), project_path, project_name
            commits.append(record)

        except Exception as er:
            print('Problem reading commit ' + hash)
            print(er)
            continue

    return commits


def build_file_commits_from_commits(commits):
    file_commits = []

    for commit in commits:
        for f in commit.pydriller_files:
            record = {
                'hash': hash,
                'message': commit.message,
                'author_name': commit.author_name,
                'author_email': commit.author_email,
                'author_date': commit.author_date,
                'author_tz': commit.author_timezone,
                'committer_name': commit.committer_name,
                'committer_email': commit.committer_email,
                'committer_date': commit.committer_date,
                'committer_tz': commit.committer_timezone,
                'in_main': commit.in_main,
                'is_merge': commit.is_merge,
                'num_deletes': commit.num_deletes,
                'num_inserts': commit.num_inserts,
                'net_lines': commit.net_lines,
                'branches': commit.branches,
                'filename': f.filename,
                'old_path': f.old_path,
                'new_path': f.new_path,
                'project_name': commit.project_name,
                'project_path': commit.project_path, 
            }
            # Omitted: modified_files (list), project_path, project_name
            file_commits.append(record)


    return file_commits


def build_file_commits(repo):
    """
    Builds a collection of commit objects for each file modified by a commit.
    This allows us to track the frequency of changes for a given file, the first modified date, and the last modified date.
    """
    commits = []

    for commit in repo.traverse_commits():
        hash = commit.hash
        try:
            # Sanitize the message to prevent it from confusing our resulting CSV
            msg = sanitize_message(commit.msg)

            # Optimization to prevent requesting same data twice
            author = commit.author
            committer = commit.committer
            inserts = commit.insertions
            deletions = commit.deletions
            author_date = commit.author_date
            author_timezone = commit.author_timezone
            committer_date = commit.committer_date
            committer_timezone = commit.committer_timezone
            in_main_branch = commit.in_main_branch
            is_merge = commit.merge
            branches = ', '.join(commit.branches) # Comma separated list of branches the commit is found in
            project_name = commit.project_name
            project_path = commit.project_path

            for f in commit.modified_files:
                record = {
                    'hash': hash,
                    'message': msg,
                    'author_name': author.name,
                    'author_email': author.email,
                    'author_date': author_date,
                    'author_tz': author_timezone,
                    'committer_name': committer.name,
                    'committer_email': committer.email,
                    'committer_date': committer_date,
                    'committer_tz': committer_timezone,
                    'in_main': in_main_branch,
                    'is_merge': is_merge,
                    'num_deletes': deletions,
                    'num_inserts': inserts,
                    'net_lines': inserts - deletions,
                    'branches': branches,
                    'filename': f.filename,
                    'old_path': f.old_path,
                    'new_path': f.new_path,
                    'project_name': project_name,
                    'project_path': project_path, 
                }
                # Omitted: modified_files (list), project_path, project_name
                commits.append(record)
        except Exception as er:
            print('Problem reading commit ' + hash)
            print(er)
            continue

    return commits

def analyze_repository(path, commits_file_path = 'Commits.csv', file_commits_file_path = 'FileCommits.csv'):
    """
    Pulls all commits from a git repository using PyDriller.
    NOTE: This can take a LONG time if there are many commits. I'm currently seeing 0.8 seconds per commit on average for remote repositories.
    """

    # Grab the repository
    print('Analyzing Git Repository at ' + path)
    repo = Repository(path)

    # Read commit data
    print('Fetching commits. This will take a long time...')
    commits = build_commits(repo)

    # Extract file commits from our commit data
    print('Fetching file commits...')
    file_commits = build_file_commits_from_commits(commits)

    # Remove temporary data
    for commit in commits:
        del commit.pydriller_files

    # Save the output data
    df_commits = pd.DataFrame(commits)
    df_commits.to_csv(commits_file_path)
    print('Saved to ' + commits_file_path)

    df_file_commits = pd.DataFrame(file_commits)
    df_file_commits.to_csv(file_commits_file_path)
    print('Saved to ' + file_commits_file_path)

    print('Repository Data Pulled Successfully')
