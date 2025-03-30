import os
import xml.etree.ElementTree as ET
import json

def extract_relevant_failure_message(full_message):
    # Check if the full_message is None
    if full_message is None:
        return ""  # Return empty string if the message is None
    
    # Check if the message starts with "Expected:" or "Expecting"
    if "expected:" in full_message:
        return full_message
    elif "expecting:" in full_message:
        return full_message
    elif "Expected" in full_message:
        return "Expected " + full_message.split("Expected")[1].strip()
    elif "Expecting" in full_message:
        return "Expecting " + full_message.split("Expecting")[1].strip()
    else:
        return full_message  # Return empty string if neither is found

def extract_relevant_error_message(error_element):
    # Get the error message from the CDATA section and strip whitespace
    error_type = error_element.get('type')
    full_message = error_element.text.strip() if error_element.text else ''

    # Isolate the relevant message before the first occurrence of " at "
    if "\n" in full_message:
        relevant_message = ""
        for line in full_message.split("\n"):
            if "at" in line and ":" in line and "(" in line and ")" in line:
                break
            relevant_message += line + "\n"
    else:
        relevant_message = full_message  # If "at" is not found, keep the full message and strip newlines

    return relevant_message.replace(error_type, "").strip("\n").strip()

def extract_method_name(test_name):
    method_name = []
    for i, char in enumerate(test_name):
        # The first character must be a letter, subsequent characters can be letters or digits
        if char.isalpha() or (i > 0 and char.isdigit()) or char == '_':
            method_name.append(char)
        else:
            break  # Stop at the first non-valid character for a method name
    return ''.join(method_name)

def get_test_identifiers(report_directory):
    passing_test_identifiers = []
    failing_test_identifiers = []

    count_pos = 0
    count_neg = 0

    for filename in os.listdir(report_directory):
        if filename.endswith(".xml") and filename.startswith("TEST-"):
            if filename.lower().endswith(".alltests.xml") and filename.lower().startswith("test-inra."):
                continue
            file_path = os.path.join(report_directory, filename)
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Iterate over all test cases
            for testcase in root.findall('testcase'):
                test_name = testcase.get('name')
                test_classname = testcase.get('classname')

                # Extract the cleaned method name
                cleaned_test_name = extract_method_name(test_name)
                # Create a unique identifier for the test (classname and method name)
                test_identifier = f"{test_classname}#{cleaned_test_name}"
                # Check for failures or errors
                if testcase.find('failure') is not None or testcase.find('error') is not None:
                    failing_test_identifiers.append(test_identifier)
                    count_neg += 1
                else:
                    passing_test_identifiers.append(test_identifier)
                    count_pos += 1
    
    # Remove duplicates by converting lists to sets and back to lists
    passing_test_identifiers = list(set(passing_test_identifiers))
    failing_test_identifiers = list(set(failing_test_identifiers))

    return passing_test_identifiers, failing_test_identifiers, count_pos, count_neg

def get_test_identifiers_and_exception(report_directory):
    passing_test_identifiers = []
    failing_test_identifiers = {}

    count_neg = 0
    count_pos = 0

    for filename in os.listdir(report_directory):
        if filename.endswith(".xml") and filename.startswith("TEST-"):
            if filename.lower().endswith(".alltests.xml") and filename.lower().startswith("test-inra."):
                continue
            file_path = os.path.join(report_directory, filename)
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Iterate over all test cases
            for testcase in root.findall('testcase'):
                test_name = testcase.get('name')
                test_classname = testcase.get('classname')

                # Extract the cleaned method name
                cleaned_test_name = extract_method_name(test_name)
                # Create a unique identifier for the test (classname and method name)
                test_identifier = f"{test_classname}#{cleaned_test_name}"

                # Check for failures or errors
                if testcase.find('failure') is not None:
                    testcase_details = testcase.find('failure')
                    if failing_test_identifiers.get(test_identifier):
                        failing_test_identifiers[test_identifier].append(
                            {
                                "type": testcase_details.get('type'),
                                "message": extract_relevant_failure_message(testcase_details.get('message')) if testcase_details.get('message') else extract_relevant_error_message(testcase_details)
                            }
                        )
                    else:
                        failing_test_identifiers[test_identifier] = [
                            {
                                "type": testcase_details.get('type'),
                                "message": extract_relevant_failure_message(testcase_details.get('message')) if testcase_details.get('message') else extract_relevant_error_message(testcase_details)
                            }
                        ]
                    count_neg += 1
                elif testcase.find('error') is not None:
                    testcase_details = testcase.find('error')
                    error_message = extract_relevant_error_message(testcase_details)
                    
                    if failing_test_identifiers.get(test_identifier):
                        failing_test_identifiers[test_identifier].append(
                            {
                                "type": testcase_details.get('type'),
                                "message": error_message
                            }
                        )
                    else:
                        failing_test_identifiers[test_identifier] = [
                            {
                                "type": testcase_details.get('type'),
                                "message": error_message
                            }
                        ]
                    count_neg += 1 
                else:
                    passing_test_identifiers.append(test_identifier)
                    count_pos += 1
    
    # Remove duplicates by converting lists to sets and back to lists
    passing_test_identifiers = list(set(passing_test_identifiers))
    
    return passing_test_identifiers, failing_test_identifiers, count_pos, count_neg


# ======================================================================================================
# ======================================================================================================
# ======================================================================================================
# ======================================================================================================
# def update_meta_data(meta_data_path, bug_id, passing_tests, failing_tests, count_pos, count_neg):
#     # Load the existing meta-data.json
#     with open(meta_data_path, 'r') as file:
#         data = json.load(file)

#     # Update the specific bug entry based on the bug_id
#     for entry in data:
#         if entry["bug_id"] == bug_id:
#             # Update passing and failing test identifiers
#             entry["passing_test_identifiers"] = passing_tests
#             entry["failing_test_identifiers"] = failing_tests

#             # Update count_pos and count_neg
#             entry["count_pos"] = count_pos
#             entry["count_neg"] = count_neg
#             break

#     # Write the updated data back to meta-data.json
#     with open(meta_data_path, 'w') as file:
#         json.dump(data, file, indent=4)

# if __name__ == "__main__":
#     # meta_data_path = "./regressionbug4apr.json"  # Update with actual path
#     metadata_path          = "./meta-data.json"
#     regressionbug4apr_path = "./regressionbug4apr.json"

#     for i in range(1, 96):
#         bug_id = "RegressionBug-" + str(i)

#         # Directory containing the Surefire XML reports for the current bug
#         report_directory = f"/home/student.unimelb.edu.au/anhh1/working-space/APR/miner_space/cache/{bug_id}/BUGGY/target/surefire-reports"
#         if i == 56 or i == 57:
#             report_directory = f"/home/student.unimelb.edu.au/anhh1/working-space/APR/miner_space/cache/{bug_id}/BUGGY/build/test-results/test"

#         # Call the function to get test identifiers
#         passing_test_identifiers, failing_test_identifiers, count_pos, count_neg = get_test_identifiers_and_exception(report_directory)
        
#         with open(regressionbug4apr_path, 'r') as file:
#             data = json.load(file)
#         for entry in data:
#             if data[entry]["bug_id"] == bug_id:
#                 data[entry]["failing_tests"] = failing_test_identifiers
#                 list_of_passing_tests = list(failing_test_identifiers.keys())
#                 list_of_failing_tests = passing_test_identifiers
#                 update_meta_data(metadata_path, bug_id, list_of_passing_tests, list_of_failing_tests, len(list_of_passing_tests), len(list_of_failing_tests))
#                 break
#         # Write the updated JSON data back to the file
#         with open(regressionbug4apr_path, 'w') as file:
#             json.dump(data, file, indent=4)
    
    # passing_test_identifiers, failing_test_identifiers, count_pos, count_neg = get_test_identifiers_and_exception("/home/student.unimelb.edu.au/anhh1/working-space/APR/miner_space/cache/RegressionBug-68/BIC/target/surefire-reports")
    # print(f"===================== RegressionBug-68 =========================")
    # print(f"Passing Tests: {count_pos}")
    # print(f"Failing Tests: {count_neg}")
    # for test_id, test_details in failing_test_identifiers.items():
    #     print("-----------------------------------------")
    #     print(f"Test: {test_id}")
    #     print(f"Type: {test_details['type']}")
    #     print(f"Message: {test_details['message']}")