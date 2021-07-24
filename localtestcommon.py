import json
import os
import paramiko
import webbrowser
from getpass import getpass
from colorama import Fore

VERSION = "1.3.2"
SETUPS_VERSION = "2021.07.24.1"

CONFIG_FILE = "localtest.json"
ADDRESS = "login.cse.unsw.edu.au"
TEMP_FOLDER =  "~/Documents/LocaltestTemp"
UPLOAD_FOLDER = "~/Documents/LocaltestUpload"

PROJECT_GITHUB = "https://github.com/MiguelGuthridge/CSE-Localtest"

UNSW_TERM = "21T2"

def getJson() -> dict:
    try:
        return json.load(open(CONFIG_FILE))
    except IOError:
        print(f"This folder is missing a {CONFIG_FILE} file.\n"
              f"Run {Fore.CYAN}localtest setup [course] [project]{Fore.RESET} to rectify")
        exit(1)

def getZidPass():
    zid = input("zID: ")
    password = getpass("Password: ")
    return zid, password

def createSsh(usr, pwd):
    # SSH into CSE
    print("Connecting SSH...")
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(ADDRESS, username=usr, password=pwd)
    except paramiko.SSHException:
        print("An error occurred while connecting to CSE Servers")
        print("Are your username and password correct?")
        exit(1)
    return ssh

def printOutput(result):
    streams = ["stdout", "stderr"]
    colours = [Fore.YELLOW, Fore.RED]
    for i, (stream, colour) in enumerate(zip(streams, colours)):
        if len(result[i]):
            print(Fore.RESET + stream + ":")
            print(colour, end='')
            for line in result[i]:
                print("\t" + line[:-1])
            print("")
    if len(result[0]) == len(result[1]) == 0:
        print("[No output]")

def runCommand(ssh, dir, command, mkdir=False):
    if mkdir:
        ssh.exec_command(f"mkdir {dir} -p\n")
    res = ssh.exec_command(f"cd {dir} && {command}\n")
    return (res[1].readlines(), res[2].readlines())

def uploadFiles(usr, pwd, folder):
    # FIXME: Use more secure system than this
    print(f"Uploading files to \"{folder}\"...")
    os.system(f"sshpass -p '{pwd}' rsync --copy-links -r ./* {usr}@{ADDRESS}:{folder}")

def downloadFiles(usr, pwd, folder, overwrite=False):
    keep = "" if overwrite else "--ignore-existing"
    print("Downloading files...")
    os.system(f"sshpass -p '{pwd}' rsync {keep} --copy-links -r {usr}@{ADDRESS}:{folder}/* .")

def removeFiles(ssh, folder):
    print("Removing temporary files...")
    ssh.exec_command(f"rm -r {folder}")
    
def launchURL(url):
    webbrowser.open(url)
    
def viewSubmissions(course, term):
    webbrowser.open(f"https://cgi.cse.unsw.edu.au/~cs{course}/{term}/flask.cgi/student/")
