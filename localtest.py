#!/bin/python3

import argparse
import json
import sys
import os

from colorama import Fore

import test, give, projectsetup
import localtestcommon as c

def badArgs():
    print(f"Run `localtest help` for help")
    exit()

def help():
    r = Fore.RESET
    d = Fore.RED
    b = Fore.CYAN
    m = Fore.MAGENTA
    y = Fore.YELLOW
    l = Fore.BLUE
    
    print('\n'.join([
        f"{b}localtest{r}: A program so that you don't need to VLab anymore",
        f"",
        f"Commands:",
        f" {y}*{r} {b}help{r}:     Display this message",
        f" {y}*{r} {b}setup{r}:    Generate required files for using localtest with a project",
        f"             and fetch starter code if necessary",
        f"             Args:",
        f"              * course: course code (eg {m}1511{r})",
        f"              * project: project to start (eg {m}lab01{r})",
        f" {y}*{r} {b}fetch{r}:    Fetch starter code (use this after setting up a custom template)",
        f" {y}*{r} {b}instruct{r}: Launch instructions for project in web browser",
        f" {y}*{r} {b}subs{r}:     View course submissions in a web browser",
        f" {y}*{r} {b}test{r}:     Run autotests on project",
        f"             Args:",
        f"              * exercises: specific exercises to test (defaults to all)",
        f" {y}*{r} {b}give{r}:     Submit code from project",
        f"             Args:",
        f"              * exercises: specific exercises to submit (defaults to all)",
        f" {y}*{r} {b}upload{r}:   Uploads the contents of the directory to VLab",
        f" {y}*{r} {b}update{r}:   Runs a {b}git pull{r} to update the repository provided that it",
        f"             was {b}git clone{r}d",
        f"",
        f"Note that for most commands, a {b}-v{r} argument will cause all output to be displayed",
        f"(eg. {b}test{r} or {b}give{r} output), even if it succeeded",
        f""
        ]))
    print('\n'.join([
        f"{r}NOTICE{r}: this program is provided in the hope that it will be useful,",
        f"however, although all reasonable efforts have been made to ensure it works,",
        f"no guarantees are made that it is flawless or infallible.",
        f"{d}This software is not endorsed by UNSW, and as such, you use it at your",
        f"own risk{r}. However, all feedback and contributions towards improving",
        f"the software would be greatly appreciated. Feel free to contribute setups",
        f"for your courses, or improvements to the app's functionality.",
        f""
    ]))
    print(f"GitHub: {l}{c.PROJECT_GITHUB}{r}")
    print(f"Version: {m}{c.VERSION}{r}")
    print(f"Setups library version: {m}{c.SETUPS_VERSION}{r}")
    print(f"Author: {b}Miguel Guthridge{r}")

def projecthelp():
    proj = c.getJson()
    try:
        c.launchURL(proj["help_url"])
    except KeyError:
        print(f"Error: help URL not found for this project ({proj['course']}_{proj['project']})")

def viewSubmissions():
    proj = c.getJson()
    c.viewSubmissions(proj["course"], c.UNSW_TERM)

def upload():
    usr, pwd = c.getZidPass()
    c.uploadFiles(usr, pwd, c.UPLOAD_FOLDER)

def update():
    print("Updating localtest...")
    os.chdir(os.path.dirname(__file__))
    os.system("git pull")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        badArgs()
    
    if sys.argv[1] == "test":
        test.main(sys.argv[2:])
    elif sys.argv[1] == "give":
        give.main(sys.argv[2:])
    elif sys.argv[1] == "setup":
        projectsetup.main(sys.argv[2:])
    elif sys.argv[1] == "fetch":
        projectsetup.mainFetch(sys.argv[2:])
    elif sys.argv[1] == "instruct":
        projecthelp()
    elif sys.argv[1] == "subs":
        viewSubmissions()
    elif sys.argv[1] == "help":
        help()
    elif sys.argv[1] == "upload":
        upload()
    elif sys.argv[1] == "update":
        update()
    else:
        badArgs()
