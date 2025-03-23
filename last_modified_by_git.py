import os
import subprocess
import argparse
from datetime import datetime

def get_git_repo_root(file_path):
    """Finds the root directory of the Git repository containing the given file."""
    try:
        result = subprocess.run(
            ['git', '-C', os.path.dirname(file_path), 'rev-parse', '--show-toplevel'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        print(f"Error finding Git repo root: {e}")
    return None

def get_last_modified_time(file_path):
    try:
        # Ensure the file exists
        if not os.path.isfile(file_path):
            print(f"Error: {file_path} does not exist or is not a file.")
            return
        
        # Determine the Git repository root
        repo_root = get_git_repo_root(file_path)
        if not repo_root:
            print(f"Error: Could not determine Git repository for {file_path}")
            return
        
        # Get relative file path from the repo root
        relative_path = os.path.relpath(file_path, repo_root)
        
        # Get last commit date for the file
        result = subprocess.run(
            ['git', '-C', repo_root, 'log', '-1', '--format=%ct', '--', relative_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode == 0:
            timestamp = int(result.stdout.strip())
            modified_time = datetime.utcfromtimestamp(timestamp).isoformat() + "Z"
            return modified_time
        
    except Exception as e:
        print(f"An error occurred: {e}")