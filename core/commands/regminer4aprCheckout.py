import os
import sys
import subprocess
import threading
import time
import shutil
from core.utils.jdk import check_jdk_version

def checkout_command(regressionbug_id, working_dir):
    if check_jdk_version() == 1:
        return 1
    
    # Check if the working directory exists
    if not os.path.exists(working_dir):
        print(f"Error: The working directory {working_dir} does not exist!")
        return 1
    
    working_dir = os.path.abspath(working_dir)

    # Define the target directory for cloning
    target_directory = os.path.join(working_dir, f"RegressionBug-{regressionbug_id}")

    if os.path.exists(target_directory):
        shutil.rmtree(target_directory)

    # Create the target directory if it does not exist
    os.makedirs(target_directory, exist_ok=True)

    # Define the repository URL (you may need to modify this)
    repository_url = f"https://github.com/brojackvn/RegMiner4APR-Benchmark.git"  # Replace with your actual repository URL

    if subprocess.call(
        ["git", "clone", "--branch", f"RegressionBug-{regressionbug_id}", repository_url, target_directory],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ) != 0:
        print(f"Error: Checking out RegressionBug-{regressionbug_id} at working directory: {target_directory}!")
        shutil.rmtree(target_directory)
        return 1
    else:
        print(f"Successfully checked out RegressionBug-{regressionbug_id} at working directory: {target_directory}")
        return 0
