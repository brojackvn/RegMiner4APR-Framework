import os
import json
import subprocess
import threading
import time
from core.utils.test_report import get_test_identifiers_and_exception
from core.utils.jdk import check_jdk_version

def run_command(command, working_dir, message = None):
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
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # Start a separate thread for the spinner
    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()
    # Wait for the compiling process to complete
    process.wait()  # Wait for the process to finish
    # Wait for the spinner thread to finish
    spinner_thread.join()

def test_command(working_dir, test_case = None):
    if check_jdk_version() == 1:
        return 1
    
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
    else:    
        with open(metadata_file, 'r') as file:
            metadata = json.load(file)
            build_system = metadata.get("build_system")
            additional_command = metadata.get("additional_command")
            failing_tests = metadata.get("failing_test_identifiers")
            passing_tests = metadata.get("passing_test_identifiers")

    # Clean the project
    if build_system == "maven":
        subprocess.run(["mvn", "clean"], cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif build_system == "gradle":
        subprocess.run(["./gradlew", "clean"], cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Run test cases
    if test_case is not None:
        if test_case not in failing_tests and test_case not in passing_tests:
            print(f"Error: Test case {test_case} is not existed!")
            return 1
        else:
            run_single_test(working_dir, test_case, build_system, additional_command, True)
                # Read the test report
            _, failing_test_identifiers, count_pos, count_neg = get_test_identifiers_and_exception(os.path.join(working_dir, "target", "surefire-reports"))
            if count_neg == 0:
                print(f"\ntest case {test_case} passed at working directory: {working_dir}")
                return 0
            else:
                print(f"\ntest case {test_case} failed at working directory: {working_dir}")
                for test_id, test_details in failing_test_identifiers.items():
                    print("-----------------------------------------")
                    print(f"Test: {test_id}")
                    print(f"Type: {test_details['type']}")
                    print(f"Message: {test_details['message']}")
                return 1
    else:
        if build_system == "maven":
            if additional_command is None:
                command = ["mvn", "test"]
            elif additional_command == "checkstyle":
                command = ["mvn", "test", "-Dcheckstyle.skip"]
            elif additional_command == "xvfb":
                command = ["xvfb-run", "mvn", "test"]
        elif build_system == "gradle":
            command = ["./gradlew", "test"]
        
        for test_case in failing_tests:
            run_single_test(working_dir, test_case, build_system, additional_command, False)
        run_command(command, working_dir, f"Running all test cases at working directory: {os.path.basename(working_dir)}")
    
    # Read the test report
    _, failing_test_identifiers, count_pos, count_neg = get_test_identifiers_and_exception(os.path.join(working_dir, "target", "surefire-reports"))
    if count_neg == 0:
        print(f"\nAll test cases passed at working directory: {working_dir}")
        return 0
    else:
        print(f"\nSummary: {count_pos} test cases passed and {count_neg} test cases failed in the working directory {working_dir}")
        for test_id, test_details in failing_test_identifiers.items():
            for test_detail in test_details:
                print("-----------------------------------------")
                print(f"Test: {test_id}")
                print(f"Type: {test_detail['type']}")
                print(f"Message: {test_detail['message']}")
        return 1

def run_single_test(working_dir, test_case, build_system, additional_command, display_output = False):
    # Determine the compile command based on the build system
    if build_system == "maven":
        if additional_command is None:
            if test_case is not None:
                single_test_command = ["mvn", "test", "-Dtest=" + test_case]
        elif additional_command == "checkstyle":
            if test_case is not None:
                single_test_command = ["mvn", "test", "-Dtest=" + test_case, "-Dcheckstyle.skip"]
        elif additional_command == "xvfb":
            if test_case is not None:
                single_test_command = ["xvfb-run", "mvn", "test", "-Dtest=" + test_case]
    elif build_system == "gradle":
        if test_case is not None:
            single_test_command = ["./gradlew", "test", "-Dtest=" + test_case]
    if display_output:
        single_test_command.insert(single_test_command.index("test"), "clean")
        run_command(single_test_command, working_dir, f"Running single test case: {test_case} at working directory: {os.path.basename(working_dir)}")
    else:
        subprocess.run(single_test_command, cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)