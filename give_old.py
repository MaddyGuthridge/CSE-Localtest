#!/bin/python3
import paramiko
import argparse
from colorama import Fore

import _common as c

GIVE_CONFIG = "give.config"

def runTests(tests, unit, folder, usr, pwd):
     # SSH into CSE
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    print("Connecting SSH...")
    ssh.connect(c.ADDRESS, username=usr, password=pwd)
    
    submitted = 0
    failed = 0
    
    for t in tests:
        t = t.strip()
        print(f"Testing {t}... ", end='', flush=True)
        result = ssh.exec_command(f"cd {folder} && {unit} autotest {t}\n")[1].readlines()
        if "0 tests failed" in result[-1]:
            print(Fore.GREEN + "All tests passed", end='')
            submitted += 1
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
        print(Fore.MAGENTA + f"{skipped} skipped, " + Fore.RED + f"{failed} failed, " + Fore.GREEN + f"{submitted} passed" + Fore.RESET)

