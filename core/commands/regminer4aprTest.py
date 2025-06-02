import os
import json
import subprocess
import threading
import time
from core.utils.test_report import get_test_identifiers_and_exception
from core.utils.jdk import check_jdk_version
from core.commands.regminer4aprCompile import compile_command

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
        subprocess.call(["mvn", "clean"], cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif build_system == "gradle":
        subprocess.call(["./gradlew", "clean"], cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if compile_command(working_dir) == 1:
        return 1
    
    # Run test cases
    if test_case is not None:
        if test_case not in failing_tests and test_case not in passing_tests:
            print(f"Error: Test case {test_case} is not existed!")
            return 1
        else:
            print("=" * 80)
            print(f"Running single test case {test_case} at working directory: {working_dir}")
            print("=" * 80)
            status = run_single_test(working_dir, test_case, build_system, additional_command)
            if status == -1:
                print(f"Error: Timeout while running test case {test_case}")
                return 1
            
            # Read the test report
            if build_system == "maven":
                _, failing_test_identifiers, count_pos, count_neg = get_test_identifiers_and_exception(os.path.join(working_dir, "target", "surefire-reports"))
            else:
                _, failing_test_identifiers, count_pos, count_neg = get_test_identifiers_and_exception(os.path.join(working_dir, "build", "test-results", "test"))
            print(f"Summary of test results:")
            print(f"- Failed test cases: {count_neg}/1")
            print(f"- Passed test cases: {count_pos}/1")
            if count_neg == 0:
                print("-"*80)
                return 0
            else:
                for test_id, test_details in failing_test_identifiers.items():
                    for test_detail in test_details:
                        print("-"*80)
                        print(f"Test: {test_id}")
                        print(f"Type: {test_detail['type']}")
                        print(f"Message: {test_detail['message']}")
                return 1
    else:
        if build_system == "maven":
            if additional_command == "xvfb":
                command = ["xvfb-run", "mvn", "test", "-Drat.skip", "-Dcheckstyle.skip"]
            else:
                command = ["mvn", "test", "-Drat.skip", "-Dcheckstyle.skip"]
        elif build_system == "gradle":
            command = ["./gradlew", "test"]
        
        for test_case in failing_tests:
            status = run_single_test(working_dir, test_case, build_system, additional_command)
            if status == -1:
                print(f"Error: Timeout while running test case {test_case}")
                return 1

        print("=" * 80)
        print(f"Running all test cases at working directory: {working_dir}")
        print("=" * 80)
        try:
            subprocess.call(command, cwd=working_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            print(f"Error: Timeout while running all test cases")
            return 1
        
        # Read the test report
        if build_system == "maven":
            _, failing_test_identifiers, count_pos, count_neg = get_test_identifiers_and_exception(os.path.join(working_dir, "target", "surefire-reports"))
        else:
            _, failing_test_identifiers, count_pos, count_neg = get_test_identifiers_and_exception(os.path.join(working_dir, "build", "test-results", "test"))
        print(f"Summary of test results:")
        print(f"- Failed test cases: {count_neg}/{count_neg+count_pos}")
        print(f"- Passed test cases: {count_pos}/{count_neg+count_pos}")
        if count_neg == 0:
            print("-"*80)
            return 0
        else:
            for test_id, test_details in failing_test_identifiers.items():
                for test_detail in test_details:
                    print("-"*80)
                    print(f"Test: {test_id}")
                    print(f"Type: {test_detail['type']}")
                    print(f"Message: {test_detail['message']}")
            return 1

def run_single_test(working_dir, test_case, build_system, additional_command):
    # Determine the compile command based on the build system
    if build_system == "maven":
        if additional_command == "xvfb":
            single_test_command = ["xvfb-run", "mvn", "test", "-Dtest=" + test_case, "-Drat.skip", "-Dcheckstyle.skip"]
        else:
            single_test_command = ["mvn", "test", "-Dtest=" + test_case, "-Drat.skip", "-Dcheckstyle.skip"]
    elif build_system == "gradle":
        single_test_command = ["./gradlew", "test", "-Dtest=" + test_case]
    
    try :
        status = subprocess.call(single_test_command, cwd=working_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return 0 if status == 0 else 1
    except subprocess.TimeoutExpired:
        return -1