import json
import os
import paramiko
import webbrowser
from getpass import getpass
from colorama import Fore

VERSION = "1.2.2"
SETUPS_VERSION = "2021.06.21"

CONFIG_FILE = "localtest.json"
ADDRESS = "login.cse.unsw.edu.au"
TEMP_FOLDER =  "~/Documents/LocaltestTemp"
UPLOAD_FOLDER = "~/Documents/LocaltestUpload"

UNSW_TERM = "21T2"

def getJson() -> dict:
    try:
        return json.load(open(CONFIG_FILE))
    except IOError:
        print(f"This folder is missing a {CONFIG_FILE} file.\n"
              f"Run localtest setup [course] [project] to rectify")
        exit()

def getZidPass():
    zid = input("zID: ")
    password = getpass("Password: ")
    return zid, password

def createSsh(usr, pwd):
    # SSH into CSE
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    print("Connecting SSH...")
    ssh.connect(ADDRESS, username=usr, password=pwd)
    return ssh

def printOutput(result):
    print(Fore.YELLOW, end='')
    for line in result:
        print("\t" + line.strip())
    print("")

def runCommand(ssh, dir, command, mkdir=False):
    if mkdir:
        ssh.exec_command(f"mkdir {dir} -p\n")
    return ssh.exec_command(f"cd {dir} && {command}\n")[1].readlines()

def uploadFiles(usr, pwd, folder):
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
