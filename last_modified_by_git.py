import git
import os
import argparse
from datetime import datetime

def get_last_modified_date(file_path, repo_path):
    """Get the last modified date of a file tracked in Git"""
    
    # Ensure the file exists
    if not os.path.exists(file_path):
        print(f"❌ Error: File '{file_path}' not found.")
        return None

    # Find the Git repository root
    try:
        repo = git.Repo(repo_path, search_parent_directories=True)
    except git.exc.InvalidGitRepositoryError:
        print(f"❌ Error: '{repo_path}' is not a valid Git repository.")
        return None

    # Convert file path to a repository-relative path
    abs_file_path = os.path.abspath(file_path)
    repo_root = repo.working_dir

    if not abs_file_path.startswith(repo_root):
        print(f"❌ Error: '{file_path}' is outside the Git repository '{repo_root}'.")
        return None

    rel_file_path = os.path.relpath(abs_file_path, repo_root)

    # Get commit logs for the file
    try:
        commits = list(repo.iter_commits(paths=rel_file_path, max_count=1))
    except git.exc.GitCommandError:
        print(f"⚠️ Warning: No commit history found for '{file_path}'.")
        return None

    if not commits:
        return None
    
    if not commits:
        print(f"⚠️ Warning: No commit history found for '{file_path}'.")
        return None
    
    last_commit = commits[0]
    last_modified_date = datetime.fromtimestamp(last_commit.committed_date)

    return last_modified_date.strftime("%Y-%m-%d %H:%M:%S")