# 🛠️ Validation Usage 
This validation tool is buildt on top of the **RegMiner** tool, requiring additional criteria (as presented in our paper) to validate potential regression bugs extracted by **RegMiner**.

## 📋 Prerequisites

* **Java 11** is required to run the validation tool. However, **Java 7, 8, 11, and 17** are needed to support the validation of each bug, as each bug may require a different Java version.
* **Maven 3.9.8**
* **Gradle 4.4.1**
* **xvfb 1.20.13** (for virtual display)

## ⚙️ Usage

### 🐳 OPTION 1: Docker

#### Steps to Run the Validation Tool on Docker

1. **Prerequisites**
    
    Ensure **Docker** is installed and running on your system.

2. **Clone the repository**
    ```bash
    git clone hhttps://github.com/MSR25-RegressionBug/RegMiner4APR-Framework.git
    ```

3. **Build Docker image**
    ```bash
    cd regression-validation
    wget https://figshare.com/ndownloader/files/50177778 -O ./jdk-7u80-linux-x64.tar.gz
    docker build -t regression-validation .
    ```

4. **Validating a Potential Regression Bug**

    ```bash
    docker run --rm -it regression-validation \
        java -jar regminer4apr-validation.jar regressionbug \
        -rp w3c/epubcheck \
        -w /tmp \
        -t com.adobe.epubcheck.api.Epub30CheckExpandedTest#testIssue922 \
        -bic 25c0b3726c7284596a87551b82128fa41b636662 \
        -bfc 4e17714866ca4e8b183e001badf7bd5fd63f2216 \
        -id Example-Validation-RegressionBug
    ```

    ```bash
    docker run --rm -it regression-validation \
        java -jar regminer4apr-validation.jar regressionbug4apr \
        -rp w3c/epubcheck \
        -w /tmp \
        -t com.adobe.epubcheck.api.Epub30CheckExpandedTest#testIssue922 \
        -bic 25c0b3726c7284596a87551b82128fa41b636662 \
        -bfc 4e17714866ca4e8b183e001badf7bd5fd63f2216 \
        -id Example-Validation-RegressionBug
    ```

    **Parameters:**
    - Two modes:
        - `regressionbug`: Validates a set of bug-inducing commits, bug-fixing commits, and test cases.
        - `regressionbug4apr`: Similar to `regressionbug`, but ensures that the buggy commit fails the regression bug-witnessing test cases, while the bug-fixing commit successfully passes all test cases.
    - `-rp`: Repository path, such as `alibaba/fastjson`.
    - `-w`: Working directory, e.g., `/tmp`.
    - `-t`: Test case identifier.
    - `-bic`: Bug-Inducing Commit SHA.
    - `-bfc`: Bug-Fixing Commit SHA.
    - `-id`: ID for this validation instance. This identifier creates a directory (e.g., `/tmp/Example-Validation-RegressionBug`) that contains four commit versions if the bug is validated as a regression bug: *working*, *bug-inducing*, *buggy*, and *bug-fixing commits*.


### 💻 OPTION 2: Local Machine (Linux is required)

#### Steps to Run the Validation Tool Locally

1. **Extract the JAR Files**

    Create a directory for the validation tool and extract the JAR files:

    ```bash
    mkdir regminer4apr-validation
    cd regminer4apr-validation
    jar xf ../regminer4apr-validation.jar
    ```

2. **Validating a Potential Regression Bug**

    Make sure **Java 11** is set as the default version. You can verify this by checking the version:

    ```bash
    java --version
    ```

    #### Example Command for Validation

    Use the following example command to validate a specific regression bug:

    ```bash
    java -jar regminer4apr-validation.jar regressionbug \
        -rp w3c/epubcheck \
        -w /tmp \
        -t com.adobe.epubcheck.api.Epub30CheckExpandedTest#testIssue922 \
        -bic 25c0b3726c7284596a87551b82128fa41b636662 \
        -bfc 4e17714866ca4e8b183e001badf7bd5fd63f2216 \
        -id Example-Validation-RegressionBug
    ```

    ```bash
    java -jar regminer4apr-validation.jar regressionbug4apr \
        -rp w3c/epubcheck \
        -w /tmp \
        -t com.adobe.epubcheck.api.Epub30CheckExpandedTest#testIssue922 \
        -bic 25c0b3726c7284596a87551b82128fa41b636662 \
        -bfc 4e17714866ca4e8b183e001badf7bd5fd63f2216 \
        -id Example-Validation-RegressionBug
    ```

    **Parameters:**
    - Two modes:
        - `regressionbug`: Validates a set of bug-inducing commits, bug-fixing commits, and test cases.
        - `regressionbug4apr`: Similar to `regressionbug`, but ensures that the buggy commit fails the regression bug-witnessing test cases, while the bug-fixing commit successfully passes all test cases.
    - `-rp`: Repository path, such as `alibaba/fastjson`.
    - `-w`: Working directory, e.g., `/tmp`.
    - `-t`: Test case identifier.
    - `-bic`: Bug-Inducing Commit SHA.
    - `-bfc`: Bug-Fixing Commit SHA.
    - `-id`: ID for this validation instance. This identifier creates a directory (e.g., `/tmp/Example-Validation-RegressionBug`) that contains four commit versions if the bug is validated as a regression bug: *working*, *bug-inducing*, *buggy*, and *bug-fixing commits*.

3. After running the command, it will replicate the regression bug at `/tmp/Example-Validation-RegressionBug`, including 4 commit versions, migrated test cases, and their dependencies (if it is actual regression bug).