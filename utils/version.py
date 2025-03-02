import subprocess
import os
import streamlit as st
from utils.logger import log_function_call

@log_function_call
@st.cache_data
def get_git_version(module_path=None):
    """Get the version based on Git commits and merges.

    - If `module_path` is provided, count commits only for that module.
    - Otherwise, count commits globally for the repository.
    """
    # log current file and path
    try:
        # Base Git command
        base_cmd = ["git", "rev-list", "--count", "HEAD"]

        # If module_path is specified, restrict commit
        # history to that directory
        if module_path and os.path.isdir(module_path):
            base_cmd.extend(["--", module_path])

        # Count total commits in the specified module (or whole repo)
        commit_count = subprocess.check_output(base_cmd, text=True).strip()

        # Count merges into main (only applies globally, not per module)
        pr_count = subprocess.check_output(
            ["git", "rev-list", "--count", "--merges", "main"],
            text=True
        ).strip()

        return f"v{pr_count}.{commit_count}"
    except subprocess.CalledProcessError:
        return "v0.0"  # Fallback version if Git fails


# if __name__ == "__main__":
#     print(get_git_version())  # Print repo-wide version
