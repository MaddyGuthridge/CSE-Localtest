import argparse
from colorama import Fore

import localtestcommon as c

def runTests(tests, subsets, course, ssh, verbose):
    t_pass = 0
    t_fail = 0
    t_skip = 0

    if len(subsets) == 0:
        subsets = [None]

    for t in tests:
        print(f"Testing exercise: {t['name']} ({t['identifier']})... ", end='', flush=True)
        for s in subsets:
            if s is None:
                s = ""
            else:
                print(f"\n - {s}... ", end='', flush=True)
            
            doOutput = verbose is not None
            cmd = f"{course} autotest {t['identifier']} {s} {' '.join(t['files'])}"
            #print(cmd)
            output = c.runCommand(ssh, c.TEMP_FOLDER, cmd)
            if len(output[0]):
                if "could not be run" in output[0][-1]:
                    print(Fore.MAGENTA + "Some tests could not be run")
                    doOutput = True
                    t_skip += 1
                elif " 0 tests failed" in output[0][-1]:
                    print(Fore.GREEN + "All tests passed")
                    t_pass += 1
                else:
                    print(Fore.RED + "Not all tests passed")
                    doOutput = True
                    t_fail += 1
            else:
                print("An error occurred while running tests")
                t_skip += 1
                doOutput = True
            
            if doOutput:
                c.printOutput(output)
            print(Fore.RESET, end='')
    
    if t_fail == t_skip == 0:
        print(Fore.GREEN + "All exercises passed!!!")
    else:
        print("Overall: " + Fore.MAGENTA + f"{t_skip} skipped, " + Fore.RED + f"{t_fail} failed, " + Fore.GREEN + f"{t_pass} passed" + Fore.RESET)

    print(Fore.RESET, end='')

def parseTests(arg_tests, config):
    if len(arg_tests) == 0:
        print("Testing all exercises")
        test_list = config["exercises"]
    else:
        test_list = []
        for t in config["exercises"]:
            if t["identifier"] in arg_tests:
                test_list.append(t)
                arg_tests.remove(t["identifier"])
        if len(arg_tests) > 0:
            # "Unable to find definitions for *n* exercise(s)"
            print(f"Unable to find definitions for {len(arg_tests)} "
                  f"exercise{'' if len(arg_tests) == 1 else 's'}:")
            for t in arg_tests:
                print(" - " + t)
    
    # Check there are actually tests
    if len(test_list) == 0:
        print("Error: no tests are defined for this exercise")
        print("Create some in localtest.json")
        exit(1)
    
    return test_list

def parseSubsets(subsets, test_list):
    # Ensure subsets are valid
    if subsets is None:
        return []
    # Can't do subsets for tests on multiple exercises
    if len(test_list) > 1:
        print("Error: can't test subsets for multiple exercises")
        exit(1)
    
    # Check subsets are allowed
    e = test_list[0]
    if "subsets" not in e:
        print(f"Error: subsets are not defined for exercise {e['name']}")
        exit(1)
    
    subset_list = []
    missing = []
    for s in subsets:
        try:
            subset_list.append(e["subsets"][s])
        except KeyError:
            missing.append(s)

    if len(missing) > 0:
        # "Unable to find definitions for *n* exercise(s)"
        print(f"Unable to find definitions for {len(missing)} "
                f"subset{'' if len(missing) == 1 else 's'}:")
        for s in subsets:
            print(" - " + s)

        if len(subset_list) == 0:
            print("No valid subsets were requested: testing entire exercise")
    return subset_list

def main(args):
    config = c.getJson()
    parser = argparse.ArgumentParser(prog="localtest test", description="Run tests for UNSW CSE courses")
    parser.add_argument("exercises", type=str, default=None, nargs="*")
    parser.add_argument("-s", "--subsets", type=str, default=None, nargs="*")
    parser.add_argument("-v", "--verbose", action="count")
    parsed = parser.parse_args(args)
    arg_tests = parsed.exercises
    arg_subsets = parsed.subsets
    verbosity = parsed.verbose
    
    print(f"Course: {config['course']}, Project: {config['project']}")
    
    tests = parseTests(arg_tests, config)
    
    subsets = parseSubsets(arg_subsets, tests)
    
    usr, pwd = c.getZidPass()
      
    c.uploadFiles(usr, pwd, c.TEMP_FOLDER)
    
    ssh = c.createSsh(usr, pwd)
    
    runTests(tests, subsets, config["course"], ssh, verbosity)
    
    c.removeFiles(ssh, c.TEMP_FOLDER)
    ssh.close()
