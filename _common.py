
import os
from getpass import getpass
from colorama import Fore

ADDRESS = "login.cse.unsw.edu.au"

def getZidPass():
    zid = input("zID: ")
    password = getpass("Password: ")
    return zid, password

def printOutput(result):
    print(Fore.YELLOW, end='')
    for line in result:
        print("\t" + line.strip())

def uploadFiles(usr, pwd, folder):
    print("Uploading files...")
    os.system(f"sshpass -p '{pwd}' rsync -r ./* {usr}@{ADDRESS}:{folder}")

def removeFiles(ssh, folder):
    print("Removing residue files...")
    ssh.exec_command(f"rm -r {folder}")
    
