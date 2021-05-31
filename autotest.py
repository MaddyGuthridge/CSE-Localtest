#!/bin/python3
import paramiko
import argparse
from colorama import Fore

import _common as c

AUTOTEST_CONFIG = "autotest.config"

def runTests(tests, unit, folder, usr, pwd):
     # SSH into CSE
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    print("Connecting SSH...")
    ssh.connect(c.ADDRESS, username=usr, password=pwd)
    
    passed = 0
    failed = 0
    skipped = 0
    
    for t in tests:
        t = t.strip()
        print(f"Testing {t}... ", end='', flush=True)
        result = ssh.exec_command(f"cd {folder} && {unit} autotest {t}\n")[1].readlines()
        if "could not be run" in result[-1]:
            print(Fore.MAGENTA + "Some tests could not be run")
            c.printOutput(result)
            skipped += 1
        elif "0 tests failed" in result[-1]:
            print(Fore.GREEN + "All tests passed", end='')
            passed += 1
        else:
            print(Fore.RED + "Not all tests passed")
            c.printOutput(result)
            failed += 1
            
        print(Fore.RESET)
    
    c.removeFiles(ssh, folder)
    ssh.close()
    if failed == skipped == 0:
        print(Fore.GREEN + "All exercises passed!!!")
    else:
        print(Fore.MAGENTA + f"{skipped} skipped, " + Fore.RED + f"{failed} failed, " + Fore.GREEN + f"{passed} passed" + Fore.RESET)

def main(course, tests):
    folder = "~/Documents/SSH-Autotest"
    usr, pwd = c.getZidPass()
    c.uploadFiles(usr, pwd, folder)
    
    if tests is None:
        with open(AUTOTEST_CONFIG) as f:
            tests = f.readlines()
    
    tests = [t.strip() for t in tests]
    runTests(tests, course, folder, usr, pwd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run autotests or do submission for a program for UNSW CSE")
    parser.add_argument("course", type=int, help="Course code (eg 1511)")
    parser.add_argument("--test", type=str, nargs='+', default=None, help="Specify individual exercises to be tested\n"
                                                                          "Default: all tests in local file `autotest.config`")
    args = parser.parse_args()
    main(args.course, args.test)
