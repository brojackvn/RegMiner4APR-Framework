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
            java_version = metadata.get("java_version")
            bug_id = metadata.get("bug_id")
            failing_tests = metadata.get("failing_test_identifiers")
            passing_tests = metadata.get("passing_test_identifiers")

    # Prepare environment
    env = os.environ.copy()
    # Determine the clean command based on the build system
    if int(java_version) == 8:
        java_home = "/usr/lib/jvm/java-8-openjdk-amd64"
    elif int(java_version) == 11:
        java_home = "/usr/lib/jvm/java-11-openjdk-amd64"
    else:
        print(f"Error: Unsupported Java version: {java_version}")
        return 1
    env["JAVA_HOME"] = java_home
    env["PATH"] = f"{java_home}/bin:" + env["PATH"]

    # Clean the project
    if build_system == "maven":
        subprocess.call(["mvn", "clean"], env=env, cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif build_system == "gradle":
        subprocess.call(["./gradlew", "clean"], env=env, cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Run test cases
    if test_case is not None:
        if test_case not in failing_tests and test_case not in passing_tests:
            print(f"Error: Test case {test_case} is not existed!")
            return 1
        else:
            # Exception for some bugs that the framework does not support running single test case
            if bug_id == "RegressionBug-119" or bug_id == "RegressionBug-129" or bug_id == "RegressionBug-131" or bug_id == "RegressionBug-134":
                print(f"Framework does not support running single test case for {bug_id}!")
                return 1
            
            # Compile the project
            if compile_command(working_dir) == 1:
                return 1
            
            # Run the single test case
            print("=" * 80)
            print(f"Running single test case {test_case} at working directory: {working_dir}")
            print("=" * 80)
            status = run_single_test(working_dir, test_case, build_system, env, bug_id)
            if status == -1:
                print(f"Error: Timeout while running test case {test_case}")
                return 1
            
            # Read the test report
            if build_system == "maven":
                if bug_id == "RegressionBug-117" or bug_id == "RegressionBug-118":
                    _, failing_test_identifiers, count_pos, count_neg = get_test_identifiers_and_exception(os.path.join(working_dir, "gson", "target", "surefire-reports"))
                else:
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
        # Compile the project
        if compile_command(working_dir) == 1:
            return 
        
        # Determine the test command based on the build system
        if build_system == "maven":
            if bug_id == "RegressionBug-23":
                command = ["xvfb-run", "mvn", "test", "-Drat.skip", "-Dcheckstyle.skip"]
            elif bug_id == "RegressionBug-119":
                command = ["mvn", "-pl", "dbus-java-utils", "-am", "test"]
            elif bug_id == "RegressionBug-129":
                command = ["mvn", "-pl", "spring-data-rest-webmvc", "test"]
            else:
                command = ["mvn", "test", "-Drat.skip", "-Dcheckstyle.skip"]
        elif build_system == "gradle":
            command = ["./gradlew", "test"]
               
        # RegressionBug-144 run only the failing tests individually due to timeout issues
        if bug_id == "RegressionBug-144":
            for test_case in failing_tests:
                status = run_single_test(working_dir, test_case, build_system, env, bug_id)
                if status == -1:
                    print(f"Error: Timeout while running test case {test_case}")
                    return 1
        else:
            for test_case in failing_tests:
                status = run_single_test(working_dir, test_case, build_system, env, bug_id)
                if status == -1:
                    print(f"Error: Timeout while running test case {test_case}")
                    return 1

            print("=" * 80)
            print(f"Running all test cases at working directory: {working_dir}")
            print("=" * 80)
            try:
                subprocess.call(command, cwd=working_dir, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.TimeoutExpired:
                print(f"Error: Timeout while running all test cases")
                return 1
        
        # Read the test report
        if build_system == "maven":
            if bug_id == "RegressionBug-117" or bug_id == "RegressionBug-118":
                _, failing_test_identifiers, count_pos, count_neg = get_test_identifiers_and_exception(os.path.join(working_dir, "gson", "target", "surefire-reports"))
            elif bug_id == "RegressionBug-119":
                _, failing_test_identifiers, count_pos, count_neg = get_test_identifiers_and_exception(os.path.join(working_dir, "dbus-java-utils", "target", "surefire-reports"))
            elif bug_id == "RegressionBug-129":
                _, failing_test_identifiers, count_pos, count_neg = get_test_identifiers_and_exception(os.path.join(working_dir, "spring-data-rest-webmvc", "target", "surefire-reports"))
            else:
                _, failing_test_identifiers, count_pos, count_neg = get_test_identifiers_and_exception(os.path.join(working_dir, "target", "surefire-reports"))
        elif build_system == "gradle":
            if bug_id == "RegressionBug-131":
                _, failing_test_identifiers, count_pos, count_neg = get_test_identifiers_and_exception(os.path.join(working_dir, "spring-rabbit", "build", "test-results", "test"))
            elif bug_id == "RegressionBug-134":
                _, failing_test_identifiers, count_pos, count_neg = get_test_identifiers_and_exception(os.path.join(working_dir, "spring-amqp", "build", "test-results", "test"))
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

def run_single_test(working_dir, test_case, build_system, env, bug_id):
    # Determine the compile command based on the build system
    if build_system == "maven":
        if bug_id == "RegressionBug-23":
            single_test_command = ["xvfb-run", "mvn", "test", "-Dtest=" + test_case, "-Drat.skip", "-Dcheckstyle.skip"]
        elif bug_id == "RegressionBug-119":
            single_test_command = ["mvn", "-pl", "dbus-java-utils", "-am", "-Dtest=" + test_case, "-DfailIfNoTests=false", "test"]
        elif bug_id == "RegressionBug-129":
            single_test_command = ["mvn", "-pl", "spring-data-rest-webmvc", "-Dtest=" + test_case, "test"]
        else:
            single_test_command = ["mvn", "test", "-Dtest=" + test_case, "-Drat.skip", "-Dcheckstyle.skip"]
    elif build_system == "gradle":
        if bug_id == "RegressionBug-131":
            single_test_command = ["./gradlew", ":spring-rabbit:test", "--tests", test_case, "--refresh-dependencies"]
        elif bug_id == "RegressionBug-134":
            single_test_command = ["./gradlew", ":spring-amqp:test", "--tests", test_case, "--refresh-dependencies"]
        else:
            single_test_command = ["./gradlew", "test", "-Dtest=" + test_case]
    
    try :
        status = subprocess.call(single_test_command, env=env, cwd=working_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return 0 if status == 0 else 1
    except subprocess.TimeoutExpired:
        return -1