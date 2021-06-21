import os
import shutil
import argparse

import localtestcommon as c


def getStarterCode(overwrite):
    config = c.getJson()
    if "starter_code" in config:
        print("Fetching starter code...")
        usr, pwd = c.getZidPass()
        ssh = c.createSsh(usr, pwd)
        c.runCommand(ssh, c.TEMP_FOLDER, config["starter_code"], mkdir=True)
        c.downloadFiles(usr, pwd, c.TEMP_FOLDER, overwrite)
        c.removeFiles(ssh, c.TEMP_FOLDER)
        ssh.close()
    else:
        print("No starter code found")

def getSetupJson(course, project):
    f_dir = os.path.dirname(__file__) + "/setups/" + str(course) + "/" + project + ".json"
    if os.path.exists(f_dir):
        print("Creating localtest.json...")
        shutil.copyfile(f_dir, "localtest.json")
    else:
        print(f"Error: setup configuration for {course}/{project} not found")
        exit(0)

def getDefaultJson():
    f_dir = os.path.dirname(__file__) + "/setups/" + "default.json"
    if os.path.exists(f_dir):
        print("Creating localtest.json...")
        shutil.copyfile(f_dir, "localtest.json")
    else:
        print("Error: default.json missing!")

def checkDirContents():
    """Return whether to overwrite existing files
    """
    # Check if directory has files or folders (excluding localtest.json)
    for root, _, files in os.walk("."):
        for name in files:
            if os.path.join(root, name) != os.path.join(".", "localtest.json"):
                # We found a file that wasn't localtest.json
                print("Warning: the directory already has files or folders present")
                print("Choose one:\n"
                    "  'o': overwrite existing files\n"
                    "  'k': keep existing files\n"
                    "  'c': cancel (default)")
                #print("Note that localtest.json will always be overwritten")
                choice = input()
                if choice == 'o':
                    return True
                elif choice == 'k':
                    return False
                else:
                    exit()
    # End of loop: nothing found if we didn't return already
    return False

def main(args):
    if len(args) > 0 and args[0] == "default":
        checkDirContents()
        getDefaultJson()
        exit()
    parser = argparse.ArgumentParser("localtest setup", description="Set up a directory to work with localtest")
    parser.add_argument("course", type=str)
    parser.add_argument("project", type=str)
    args = parser.parse_args(args)
    overwrite = checkDirContents()
    getSetupJson(args.course, args.project)
    getStarterCode(overwrite)

def mainFetch(args):
    overwrite = checkDirContents()
    getStarterCode(overwrite)
