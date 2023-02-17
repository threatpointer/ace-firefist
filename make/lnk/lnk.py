import argparse
import io
import os, sys

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import lib.pylnk3.helpers
from model import AceFile, PluginDecorator


@PluginDecorator
def makeLnk(name: str, target: str, arguments: str) -> bytes:
    lnk = lib.pylnk3.helpers.for_file(target, lnk_name=name, arguments=arguments, is_file=True)
    lnkFileData = io.BytesIO()
    lnk.write(lnkFileData)
    return lnkFileData.getvalue()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', help='target path')
    parser.add_argument('--arguments', help='arguments')
    parser.add_argument('--name', help='lnk filename to create')
    args = parser.parse_args()

    lnkData = makeLnk(
        args.name,
        args.target,
        args.arguments,
    )

    # python3 -m make.lnk.lnk --name shortcut.lnk --target C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe --arguments "-noexit -command ls"    
    file = open(args.name, 'wb')
    file.write(lnkData)
    file.close()


if __name__ == "__main__":
    main()