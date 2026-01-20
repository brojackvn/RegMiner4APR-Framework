import json
import os

def get_bug_by_id(regressionbug_id):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(current_dir, "../../regressionbug4apr.json"), "r") as file:
        regressionbug4apr = json.load(file)
    with open(os.path.join(current_dir, "../../meta-data.json"), "r") as file:
        meta_data = json.load(file)
    
    info_regressionbug = []
    for bug in regressionbug4apr:
        if regressionbug4apr[bug]["bug_id"] == f"RegressionBug-{regressionbug_id}":
            info_regressionbug.append(regressionbug4apr[bug])
    for bug in meta_data:
        if bug["bug_id"] == f"RegressionBug-{regressionbug_id}":
            info_regressionbug.append(bug)
    
    return info_regressionbug

def info_command(regressionbug_id):
    regressionbug4apr, meta_data = get_bug_by_id(regressionbug_id)
    print("=" * 80)
    print(f"Summary of RegressionBug-{regressionbug_id}:")
    print("-" * 80)
    print(f"Github repository     : {regressionbug4apr['github_repository']}")
    print(f"Bug fixing commit id  : {regressionbug4apr['bfcID']}")
    print(f"Buggy commit id       : {regressionbug4apr['buggyID']}")
    print(f"Bug inducing commit id: {regressionbug4apr['bicID']}")
    print(f"Working commit id     : {regressionbug4apr['workingID']}")
    print("-" * 80)
    print(f"Java version          : {meta_data['java_version']}")
    print(f"Build system          : {meta_data['build_system']}")
    print("-" * 80)
    print(f"The number of test cases       : {meta_data['count_neg'] + meta_data['count_pos']}")
    print(f"The number of failed test cases: {meta_data['count_neg']}")
    print(f"List of failed test cases:")
    for key, items in regressionbug4apr["failing_tests"].items():
        print(f"  - {key}")
        for item in items:
            print(f"    -> Type   : {item['type']}")
            print(f"    -> Message: {item['message']}")
    return 0

    
