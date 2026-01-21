import subprocess

# Function to get JDK version
def check_jdk_version():
    try:
        result = subprocess.run(['java', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Check if the output contains 'version "1.8'
        if 'version "1.8' in result.stderr or 'version "8' in result.stderr:
            return 0  # Java 8 is found
        elif 'version "11' in result.stderr:
            return 1  # Java 11 is found
        else:
            print("Java 8 is required!")
            return 1  # Not Java 8
    except FileNotFoundError:
        print("Java is not installed or not in the system's PATH.")
        return 1