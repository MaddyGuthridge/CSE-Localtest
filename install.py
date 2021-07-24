# Add aliases to .bash_aliases and .zhsrc

import os
import platform
from colorama import Fore

def windowsError():
    print(f"{Fore.RED}ERROR: Running Localtest on Windows is not recommended "
          "for use with CSE work")
    print(f"{Fore.RESET}Continuing to use it may produce different output "
          "from your programs compared to CSE systems")
    print("Please install Windows Subsystem for Linux using the linked"
          "instructions:")
    print("https://docs.microsoft.com/en-us/windows/wsl/install-win10")
    exit(1)

def quotePath(path: str):
    # Return path with escaped quote marks around each token with a space
    return '/'.join([r"'"+s+r"'" if ' ' in s else s
                     for s in path.split('/')])

def install():
    print("Installing localtest...")
    sys = platform.system()
    
    # Linux
    if sys == "Linux":
        print("System: Linux")

    # MacOS
    elif sys == "Darwin":
        print("System: MacOS")

    elif sys == "Windows":
        windowsError()

    # Yuck
    alias = r'alias \"localtest=\\\"' + quotePath(os.path.join(os.path.dirname(__file__), "localtest.py")) + r'\\\"\"'

    # Look for zsh config
    zsh_path = os.path.join(os.path.expanduser('~'), '.zshrc')
    if os.path.exists(zsh_path):
        print("Adding to ZSH...")
        os.system(f'sudo sh -c "echo {alias} >> {quotePath(zsh_path)}"')
    
    # Look for bash config
    bash_rc = os.path.join(os.path.expanduser('~'), '.bashrc')
    if os.path.exists(bash_rc):
        print("Adding to Bash...")
        bash_aliases = os.path.join(os.path.expanduser('~'), '.bash_aliases')
        os.system(f'sudo sh -c "echo {alias} >> {quotePath(bash_aliases)}"')
