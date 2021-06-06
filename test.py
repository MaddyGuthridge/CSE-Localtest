
import argparse
from colorama import Fore

import localtestcommon as c

def runTests(tests, course, ssh):
    t_pass = 0
    t_fail = 0
    t_skip = 0
    for t in tests:
        print(f"Testing exercise: {t['name']} ({t['identifier']})... ", end='')
        output = c.runCommand(ssh, c.TEMP_FOLDER, f"{course} autotest {t['identifier']}")
        if "could not be run" in output[-1]:
            print(Fore.MAGENTA + "Some tests could not be run")
            c.printOutput(output)
            t_skip += 1
        elif " 0 tests failed" in output[-1]:
            print(Fore.GREEN + "All tests passed", end='')
            t_pass += 1
        else:
            print(Fore.RED + "Not all tests passed")
            c.printOutput(output)
            t_fail += 1
            
        print(Fore.RESET)
    
    if t_fail == t_skip == 0:
        print(Fore.GREEN + "All exercises passed!!!")
    else:
        print(Fore.MAGENTA + f"{t_skip} skipped, " + Fore.RED + f"{t_fail} failed, " + Fore.GREEN + f"{t_pass} passed" + Fore.RESET)

    print(Fore.RESET, end='')

def main(args):
    config = c.getJson()
    parser = argparse.ArgumentParser(prog="localtest test", description="Run tests for UNSW CSE courses")
    parser.add_argument("exercises", type=str, default=None, nargs="*")
    arg_tests = parser.parse_args(args).exercises
    
    print(f"Course: {config['course']}, Project: {config['project']}")
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
            print(f"Unable to find definitions for {len(arg_tests)} exercises(s):")
            for t in arg_tests:
                print(" - " + t)
    
    usr, pwd = c.getZidPass()
      
    c.uploadFiles(usr, pwd, c.TEMP_FOLDER)
    
    ssh = c.createSsh(usr, pwd)
    
    runTests(test_list, config["course"], ssh)
    
    c.removeFiles(ssh, c.TEMP_FOLDER)
    ssh.close()
