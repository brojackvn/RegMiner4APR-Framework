import subprocess

# Function to get JDK version
def check_jdk_version():
    try:
        result = subprocess.run(['java', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Check if the output contains 'version "1.8'
        if 'version "1.8' in result.stderr or 'version "8' in result.stderr:
            return 0  # Java 8 is found
        elif 'version "11' in result.stderr:
            return 0  # Java 11 is found
        else:
            print("Java 8 and 11 is required!")
            return 1  # Not Java 8
    except FileNotFoundError:
        print("Java is not installed or not in the system's PATH.")
        return 1

def is_jdk_version_required(java_version):
    try:
        result = subprocess.run(['java', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if f'version "1.8' in result.stderr or f'version "8' in result.stderr:
            current_version = 8
        elif f'version "11' in result.stderr:
            current_version = 11
        else:
            print(f"Java {java_version} is required, but Java version is not found!")
            return 1
        
        if current_version != java_version:
            print(f"Java {java_version} is required, but Java {current_version} is found!")
            return 1
        return 0
    except FileNotFoundError:
        print("Java is not installed or not in the system's PATH.")
        return 1    