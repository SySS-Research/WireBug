import sys
import os


def check_python_version():
    version = sys.version
    cache = str(version).replace('sys.version_info(major=', '')
    nummer = cache[0]

    if nummer == "2":
        return False
    else:
        return True


def check_sudo():
    if os.geteuid() != 0:
        return False
    else:
        return True


def logo():
    return """
     __      __.__              __________
    /  \    /  \__|______   ____\______   \__ __  ____
    \   \/\/   /  \_  __ \_/ __ \|    |  _/  |  \/ ___\\
>>>>>\>>>>>>>>/|>>||>>|>\/\>>>>>/|>>>>|>>>\>>|>>/>/>/>>>>>>>
      \__/\  / |__||__|    \___  .______  /____/\___  /
           \/                  \/       \/     /_____/

by Moritz Abrell - SySS GmbH, 2019


Follow the wizard to use WireBug.
Use TAB to show possible options.
"""

