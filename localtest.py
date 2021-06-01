#!/bin/python3

import argparse
import json
import sys

import test, give, projectsetup

def badArgs():
    print(f"Run localtest -h for help")
    exit()

def help():
    pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        badArgs()
    
    if sys.argv[1] == "test":
        test.main(sys.argv[2:])
    elif sys.argv[1] == "give":
        give.main(sys.argv[2:])
    elif sys.argv[1] == "setup":
        projectsetup.main(sys.argv[2:])
    elif sys.argv[1] == "-h":
        help()
    else:
        badArgs()

