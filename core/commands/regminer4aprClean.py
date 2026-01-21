import os
import json
import subprocess
from core.utils.jdk import check_jdk_version

def clean_command(working_dir):
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
        language = metadata.get("language")
        java_version = metadata.get("java_version")

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

    if build_system == "maven":
        command = ["mvn", "clean"]
    elif build_system == "gradle":
        command = ["./gradlew", "clean"]

    # Clean the compiled files
    print("=" * 80)
    print(f"Cleaning compiled files at working directory: {os.path.abspath(working_dir)}")
    print("-" * 40)
    clean_result = subprocess.run(command, cwd=os.path.abspath(working_dir), env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if clean_result.returncode != 0:
        print(f"Error: Cleaning compiled files at working directory!")
        print("-" * 40)      
        print(clean_result.stdout)
        print("-" * 40)
        return 1
    else:
        print(f"Successfully cleaned!")
        print("=" * 80)
        return 0
    