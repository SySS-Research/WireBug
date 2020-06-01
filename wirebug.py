#!/usr/bin/env python3
import sys
import signal
from helper import check_python_version, check_sudo


def signal_handler(sig, frame):
    print("User interruption. Exiting ...")
    sys.exit()


def main():
    signal.signal(signal.SIGINT, signal_handler)

    if check_python_version():
        if check_sudo():
            from classes import Wizard
            wizard = Wizard()
            wizard.cmdloop()
        else:
            print("\033[1;31m[!]\033[0m You need to have root privileges to run this script.")
            sys.exit(1)
    else:
        print("\033[1;31m[!]\033[0m Please use python3")
        sys.exit(1)


if __name__ == "__main__":
    main()

