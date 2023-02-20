import os, sys
from base64 import b64encode
from jinja2 import Template
import logging

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from model import *

FTP_MAX_LINE_LENGTH = 230


@PluginDecorator
def makeBatFtpExec(command: AceStr, file: str="%lOcAlApPdATA%\Temp\conf.log") -> AceStr:
    if len(command) > FTP_MAX_LINE_LENGTH:
        logging.warn("makeBatFtpExec: command len {} is longer than FTP max of about {}, this will not work".format( 
            len(command), FTP_MAX_LINE_LENGTH))

    templateFile = 'ftp-exec.bat'
    with open('make/bat/' + templateFile) as f:
        template = Template(f.read())
    script = template.render(
        command=command,
        file=file,
    )
    return AceStr(script)