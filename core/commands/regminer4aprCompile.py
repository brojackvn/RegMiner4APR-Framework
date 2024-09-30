import os
import json
import subprocess
import threading
import time 
from core.utils.jdk import check_jdk_version

def run_command(command, working_dir, message):
    def spinner():
        # Define a spinner sequence
        spin_chars = ['|', '/', '-', '\\']
        idx = 0
        while process.poll() is None:  # While the process is running
            print(f"\r{message} ..... {spin_chars[idx]}", end='', flush=True)
            idx = (idx + 1) % len(spin_chars)  # Rotate through spinner characters
            time.sleep(0.1)  # Adjust the speed of the spinner

    # Use subprocess.Popen to execute the command and suppress output
    process = subprocess.Popen(
        command,
        cwd=working_dir,
        stdout=subprocess.DEVNULL,  # Suppress stdout
        stderr=subprocess.DEVNULL,   # Suppress stderr
    )

    # Start a separate thread for the spinner
    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()
    # Wait for the compiling process to complete
    process.wait()  # Wait for the process to finish
    # Wait for the spinner thread to finish
    spinner_thread.join()
    return process.returncode

def compile_command(working_dir):
    if check_jdk_version() == 1:
        return 1
    
    # Implementation of the compile command
    if working_dir is None:
        working_dir = os.getcwd()
    else:
        if not os.path.exists(working_dir):
            print(f"Error: The working directory {working_dir} does not exist!")
            return 1
        working_dir = os.path.abspath(working_dir)
    
    metadata_file = os.path.join(working_dir, "meta-data-commit-level.json")
    # Check if the meta-data file exists
    if not os.path.exists(metadata_file):
        print(f"Error: working directory {working_dir} is not the regression bug directory!")
        return 1
    
    with open(metadata_file, 'r') as file:
        metadata = json.load(file)
        build_system = metadata.get("build_system")
        additional_command = metadata.get("additional_command")

    # Determine the compile command based on the build system
    if build_system == "maven":
        if additional_command is None:
            command = ["mvn", "clean", "compile"]
            compile_testcases_command = ["mvn", "test-compile"]
        elif additional_command == "checkstyle":
            command = ["mvn", "clean", "compile", "-Dcheckstyle.skip"]
            compile_testcases_command = ["mvn", "test-compile", "-Dcheckstyle.skip"]
        elif additional_command == "xvfb":
            command = ["xvfb-run", "mvn", "clean", "compile"]
            compile_testcases_command = ["xvfb-run", "mvn", "test-compile"]
    elif build_system == "gradle":
        command = ["./gradlew", "clean", "compileJava"]
        compile_testcases_command = ["./gradlew", "compileTestJava"]
        
    if run_command(command, working_dir, f"Compiling at working directory: {os.path.basename(working_dir)}") != 0:
        print(f"\nError: Compiling at working directory: {working_dir}!")
        return 1
    else:
        print(f"\nSuccessfully compiled at working directory: {working_dir}")
        
        # Compile the test classes
        if run_command(compile_testcases_command, working_dir, f"Compiling test classes at working directory: {os.path.basename(working_dir)}") != 0:
            print(f"\nError: Compiling test classes at working directory: {working_dir}!")
            return 1
        else:
            print(f"\nSuccessfully compiled test classes at working directory: {working_dir}")
            return 0


    