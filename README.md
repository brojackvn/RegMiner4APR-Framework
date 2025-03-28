# RegMiner4APR - Regression Bugs for Automated Program Repair

**RegMiner4APR** is a framework that provides easy access to a reproducible benchmark of real-world regression bugs, including essential commands for conducting program repair experiments with minimal configuration.

## 📑 Table of Contents

* [📦 RegMiner4APR](#regminer4apr)
* [⚙️ Installation](#️installation)
* [🖥️ Command Line Usage](#️command-line-usage)
* [🚀 Example Workflow](#example-workflow)
* [🔍 Regression Bug Validation](#regression-bug-validation)

## RegMiner4APR
To support the use of RegMiner4APR, we provide the following artifacts:

1. [🛠️ RegMiner4APR - Framework](https://github.com/MSR25-RegressionBug/RegMiner4APR-Framework): The primary toolkit for accessing and experimenting with the benchmark.
2. [📂 RegMiner4APR - Benchmark](https://github.com/MSR25-RegressionBug/RegMiner4APR-Benchmark): A structured, reproducible database of real-world regression bugs.
3. [🌐 RegMiner4APR - Homepage](https://msr25-regressionbug.github.io/RegMiner4APR-Homepage) : The central hub containing detailed information for each bug in our benchmark.

[🗄️ Data availability](https://figshare.com/s/e682027596fd3224ea31): The replication package is hosted on **Figshare** for easy access and reproducibility.

## Installation

### 🐳 OPTION 1: Docker

1. Prerequisites
    
    Ensure **Docker** is installed and running on your system.

2. Clone the repository
    ```bash
    git clone https://github.com/MSR25-RegressionBug/RegMiner4APR-Framework
    ```

3. Build the Docker image
    ```bash
    cd RegMiner4APR-Framework
    docker build -t regminer4apr-benchmark .
    ```
4. Run the Docker container
    ```bash
    docker run -it regminer4apr-benchmark /bin/bash
    ```

4. Examples of executing a command within the Docker container
    ```bash
    docker run --rm -it regminer4apr-benchmark regminer4apr env
    ```
    ```bash
    docker run --rm -it regminer4apr-benchmark regminer4apr info -rb 1
    ```
### OPTION 2: Local Machine

1. Prerequisites

    * **Python 3.12**
    * **Java 8**
    * **Maven 3.9.8**
    * **Gradle 4.4.1**
    * **xvfb 1.20.13** (for virtual display)

1. Clone the Repository
    ```bash
    git clone https://github.com/MSR25-RegressionBug/RegMiner4APR-Framework.git
    ```
2. Initialize the RegMiner4APR environment
    ```bash
    cd RegMiner4APR-Framework
    source activate
    ```
3. Verify the installation
    ```bash
    regminer4apr env
    ```
## Command Line Usage
For help with available commands, use:

```bash
regminer4apr help
```

```output
usage: regminer4apr <command> [<args>]

Commands:
  help         show help message and exit
  env          display information about the system environment
  info         display information about a specific regression bug
  checkout     checkout a regression bug at a specific working directory
  compile      compile source code at a specific working directory or current directory
  test         run all test cases at a specific working directory or current directory
```

### 1. View Current Working Environment

To view the environment variables, run:

```bash
regminer4apr env
```

### 2. Retrieve Regression Bug Information

To fetch information for a specific regression bug, use the following command:

```bash
regminer4apr info --regressionbug_id|-rb <bug_id>
```

**Options:**
- `--regressionbug`, `-rb`: Specify the unique ID of the regression bug.

### 3. Checkout the Codebase for a Regression Bug

To check out the code for a given regression bug, use the following command:

```bash
regminer4apr checkout --regressionbug_id|-rb <bug_id> --working_dir|-w <path>
```

**Options:**
- `--regressionbug`, `-rb`: The unique ID of the regression bug.
- `--working_dir`, `-w`: (Optional) Specify the working directory where the code will be checked out. Defaults to current directory if not provided.

### 4. Compile the Codebase

After checking out the codebase, you can compile it using the following command:

```bash
regminer4apr compile [--working_dir|-w <path>]
```

**Options:**
- `--working_dir`, `-w`: (Optional) Specify the working directory. Defaults to current directory if not provided.

### 5. Run Tests

To run all the test cases in the checked-out codebase, use the following command:

```bash
regminer4apr test [--working_dir|-w <path>] [--test_case|-t <single_test_case>]
```


**Options:**
- `--working_dir`, `-w`: (Optional) Specify the working directory where tests should be executed. Defaults to current directory if not provided.
- `--test_case`, `-t`: (Optional) Specify a single test case to run.

## Example Workflow

Here is an example of a typical workflow using RegMiner4APR:

1. **Check environment setup**:
    ```bash
    regminer4apr env
    ```

2. **Retrieve information about a regression bug (e.g., bug ID: 1)**:
    ```bash
    regminer4apr info --regressionbug_id 1
    ```

3. **Checkout the code for regression bug 1**:
    ```bash
    regminer4apr checkout --regressionbug_id 1 --working_dir /tmp
    ```

4. **Compile the codebase**:
    ```bash
    regminer4apr compile --working_dir /tmp/RegressionBug-1/BUGGY
    ```
    or
    ```bash
    cd /tmp/RegressionBug-1/BUGGY
    regminer4apr compile
    ```

5. **Run the tests**:
    ```bash
    regminer4apr test --working_dir /tmp/RegressionBug-1/BUGGY --test_case com.adobe.epubcheck.api.Epub30CheckExpandedTest#testIssue922 
    ```
    ```bash
    regminer4apr test --working_dir /tmp/RegressionBug-1/BUGGY
    ```

    or 
    ```bash
    cd /tmp/RegressionBug-1/BUGGY
    regminer4apr test --test_case com.adobe.epubcheck.api.Epub30CheckExpandedTest#testIssue922
    regminer4apr test
    ```

## Regression Bug Validation
    
Use this section to reproduce and validate the potential regression bugs extracted by **RegMiner**. For detailed instructions, refer to the [Usage Guide](./regression-validation/VALIDATION-USAGE.md).
