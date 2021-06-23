import argparse

import localtestcommon as c

def main(args):
    # Run command given as argument
    parser = argparse.ArgumentParser(prog="localtest test", description="Run tests for UNSW CSE courses")
    parser.add_argument("command", type=str)
    parser.add_argument("-d", "--download")
    parsed = parser.parse_args(args)

    do_download = parsed.download

    usr, pwd = c.getZidPass()
    
    c.uploadFiles(usr, pwd, c.TEMP_FOLDER)
    ssh = c.createSsh(usr, pwd)
    res = c.runCommand(ssh, c.TEMP_FOLDER, parsed.command)
    c.printOutput(res)
    
    ssh.close()
    if do_download:
        c.downloadFiles(usr, pwd, c.TEMP_FOLDER, True)
