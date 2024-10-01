import os
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
    repository_url = f"https://github.com/brojackvn/RegMiner4APR-Regression-Bugs.git"  # Replace with your actual repository URL

    # Clone the repository to the target directory
    def spinner():
        # Define a spinner sequence
        spin_chars = ['|', '/', '-', '\\']
        idx = 0
        while process.poll() is None:  # While the process is running
            print(f"\rChecking out RegressionBug-{regressionbug_id} at working directory: {os.path.basename(working_dir)} ..... {spin_chars[idx]}", end='', flush=True)
            idx = (idx + 1) % len(spin_chars)  # Rotate through spinner characters
            time.sleep(0.1)  # Adjust the speed of the spinner

    process = subprocess.Popen(
        ["git", "clone", "--branch", f"RegressionBug-{regressionbug_id}", repository_url, target_directory],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Start a separate thread for updating progress
    progress_thread = threading.Thread(target=spinner)
    progress_thread.start()
    # Wait for the cloning process to complete
    process.wait()  # Wait for the process to finish
    # Wait for the progress thread to finish
    progress_thread.join()

    if process.returncode != 0:
        print(f"\nError: Checking out RegressionBug-{regressionbug_id} at working directory: {target_directory}!")
        shutil.rmtree(target_directory)
        return 1
    else:
        print(f"\nSuccessfully checked out RegressionBug-{regressionbug_id} at working directory: {target_directory}.")
        return 0
