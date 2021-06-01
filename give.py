
import argparse
from colorama import Fore

import localtestcommon as c

def runSubmissions(tests, course, project, ssh):
    t_pass = 0
    t_fail = 0
    for t in tests:
        print(f"Submitting exercise: {t['name']} ({t['identifier']})... ", end='', flush=True)
        output = c.runCommand(ssh, c.TEMP_FOLDER, f"echo $'yes\\nyes' | give cs{course} {project}_{t['identifier']} {' '.join(t['files'])}")
        
        if "Your submission is ACCEPTED" in output[-1]:
            print(Fore.GREEN + "Accepted!")
            t_pass += 1
        else:
            print(Fore.GREEN + "Declined")
            c.printOutput(output)
            t_fail += 1
        print(Fore.RESET)
    
    if t_fail == 0:
        print(Fore.GREEN + "All exercises submitted!!!")
    else:
        print(Fore.RED + f"{t_fail} failed to submit, " + Fore.GREEN + f"{t_pass} accepted" + Fore.RESET)

    print(Fore.RESET, end='')

def main(args):
    config = c.getJson()
    parser = argparse.ArgumentParser(prog="localtest give", description="Submit work for UNSW CSE courses")
    parser.add_argument("exercises", type=str, default=None, nargs="*")
    arg_tests = parser.parse_args(args).exercises
    
    print(f"Course: {config['course']}, Project: {config['project']}")
    if len(arg_tests) == 0:
        print("Submitting all exercises")
        sub_list = config["exercises"]
    else:
        sub_list = []
        for t in config["exercises"]:
            if t["identifier"] in arg_tests:
                sub_list.append(t)
                arg_tests.remove(t["identifier"])
        if len(arg_tests) > 0:
            print(f"Unable to find definitions for {len(arg_tests)} exercises(s):")
            for t in arg_tests:
                print(" - " + t)
    
    usr, pwd = c.getZidPass()
    
    # Prompt for agreement
    
    c.uploadFiles(usr, pwd, c.TEMP_FOLDER)
    
    ssh = c.createSsh(usr, pwd)
    
    runSubmissions(sub_list, config["course"], config["project"], ssh)
    
    c.removeFiles(ssh, c.TEMP_FOLDER)
    ssh.close()
