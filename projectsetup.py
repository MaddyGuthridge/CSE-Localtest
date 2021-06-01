import os
import shutil
import argparse

import localtestcommon as c

def getStarterCode():
    config = c.getJson()
    if "starter_code" in config:
        print("Fetching starter code...")
        usr, pwd = c.getZidPass()
        ssh = c.createSsh(usr, pwd)
        c.runCommand(ssh, c.TEMP_FOLDER, config["starter_code"], mkdir=True)
        c.downloadFiles(usr, pwd, c.TEMP_FOLDER)
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

def main(args):
    parser = argparse.ArgumentParser("localtest setup", description="Set up a directory to work with localtest")
    parser.add_argument("course", type=str)
    parser.add_argument("project", type=str)
    args = parser.parse_args(args)

    getSetupJson(args.course, args.project)
    getStarterCode()
