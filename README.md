## Command Line Usage
For help with available commands, use:

```bash
regminer4apr help
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
- `--test_case`, '-t': (Optional) Specify a single test case to run.

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
    regminer4apr test
    regminer4apr test --test_case com.adobe.epubcheck.api.Epub30CheckExpandedTest#testIssue922
    ```