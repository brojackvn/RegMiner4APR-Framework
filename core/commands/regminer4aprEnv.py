import os
import subprocess
from core.utils.jdk import check_jdk_version

def print_entry(key, val, val_start_col=30):
    val = val.strip()
    num_seps = val_start_col - len(key)
    print(f"{key}{'.' * num_seps}{val}")

def print_multiline_entry(key, *lines):
    print(f"{key}:")
    for line in lines:
        if line.strip() == "":
            continue
        print(f"  {line}")

def print_environment_var(var):
    val = os.getenv(var, "(none)")
    print_entry(var, val)

def env_command():
    if check_jdk_version() == 1:
        return 1
    
    print("-" * 80)
    print("                      RegMiner4APR Execution Environment ")
    print("-" * 80)
    print_environment_var("PWD")
    print_environment_var("SHELL")
    print_entry("TZ", subprocess.getoutput("cat /etc/timezone"))
    print_environment_var("JAVA_HOME")
    
    print_entry("Git version", subprocess.getoutput("git --version"))
    print_entry("Java Exec", subprocess.getoutput("which java"))
    print_entry("Java Exec Resolved", subprocess.getoutput("realpath $(which java)"))
    print_multiline_entry("Java version", *subprocess.getoutput("java -version 2>&1").splitlines())
    print_multiline_entry("Maven version", *subprocess.getoutput("mvn -version").splitlines())
    print_multiline_entry("Gradle version", *subprocess.getoutput("gradle -version").splitlines())
    print("-" * 80)
    return 0