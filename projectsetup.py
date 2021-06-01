import os
import shutil
import argparse

def getSetupJson(course, project):
    f_dir = os.path.dirname(__file__) + "/setups/" + str(course) + "/" + project + ".json"
    shutil.copyfile(f_dir, "localtest.json")

def main(args):
    parser = argparse.ArgumentParser("localtest setup", description="Set up a directory to work with localtest")
    parser.add_argument("course", type=str)
    parser.add_argument("project", type=str)
    args = parser.parse_args(args)

    getSetupJson(args.course, args.project)
