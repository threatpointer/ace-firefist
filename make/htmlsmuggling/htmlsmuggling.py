import argparse
from jinja2 import Template
from pathlib import Path
from base64 import b64encode
from model import AceFile, PluginDecorator
from pathlib import Path


@PluginDecorator
def makeHtmlSmuggling(file, template='autodownload.html') -> str:
    """Make a HTML site from template from which the file can be downloaded"""
    path = 'make/htmlsmuggling/' + template
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError

    with open(path) as f:
        template = Template(f.read())
    
    # Arguments for the template:
    # - data: is file base64 encoded
    # - filename: the filename
    data = b64encode(file.data).decode()
    renderedHtml = template.render(
        data=data,
        filename=file.name,
    )
    return renderedHtml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", help="")
    parser.add_argument("--payload_data", help="")
    parser.add_argument("--payload_name", help="")
    args = parser.parse_args()

    file = AceFile(
        args.payload_name,
        bytes(args.payload_data, 'utf-8')
    )
    htmlData = makeHtmlSmuggling(file)

    f = open(args.filename, 'w')
    f.write(htmlData)
    f.close()


if __name__ == "__main__":
    main()