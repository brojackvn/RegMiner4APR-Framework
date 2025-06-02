import os
import sys
import json
import subprocess
import threading
import time 
from core.utils.jdk import check_jdk_version

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
        if additional_command == "xvfb":
            command = ["xvfb-run", "mvn", "clean", "compile", "-Drat.skip", "-Dcheckstyle.skip"]
            compile_testcases_command = ["xvfb-run", "mvn", "test-compile", "-Drat.skip", "-Dcheckstyle.skip"]
        else:
            command = ["mvn", "clean", "compile", "-Drat.skip", "-Dcheckstyle.skip"]
            compile_testcases_command = ["mvn", "test-compile", "-Drat.skip", "-Dcheckstyle.skip"]
    elif build_system == "gradle":
        command = ["./gradlew", "clean", "compileJava"]
        compile_testcases_command = ["./gradlew", "compileTestJava"]
        
    # Compile the source code
    print("=" * 80)
    print(f"Compiling at working directory: {os.path.abspath(working_dir)}")
    print("-" * 40)
    compile_result = subprocess.run(command, cwd=os.path.abspath(working_dir), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if compile_result.returncode != 0:
        print(f"Error: Compiling at working directory!")
        print("-" * 40)      
        print(compile_result.stdout)  # Print the actual error message
        print("-" * 40)
        return 1
    else:
        print(f"Successfully compiled!")
        print("=" * 80)
        print(f"Compiling test classes at working directory: {os.path.abspath(working_dir)}")
        print("-" * 40)
        # Compile the test classes
        if subprocess.call(compile_testcases_command, cwd=os.path.abspath(working_dir), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            print(f"Error: Compiling test classes!")
            return 1
        else:
            print(f"Successfully compiled test classes!")
            return 0
                    
            # # Copy the dependencies
            # print("=" * 80)
            # print(f"Extracting all the dependencies of project: {os.path.abspath(working_dir)}")
            # print("-" * 40)
            
            # if build_system == "maven":
            #     command = ["mvn", "dependency:copy-dependencies", "-DoutputDirectory=./target/dependencies"]
            # else:
            #     command = ["./gradlew", "copyDependencies"]
            
            # result = subprocess.run(command, cwd=os.path.abspath(working_dir), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # if result.returncode != 0:
            #     print(f"Error: Extracting the dependencies!")
            #     return 1
            # else:
            #     print(f"Successfully extracted the dependencies!")
            #     return 0