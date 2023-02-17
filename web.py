from flask import Flask, send_file
import io
from urllib.parse import urlparse
import os
from typing import List

from model import *


# a View which just returns `data`
def serveData(route):
    return f"{route.data}"


def serveDownload(route):
    #filename = os.path.basename(urlparse(route.url).path)
    # TODO necessary?
    data = route.data
    if isinstance(data, str):
        data = bytes(data, 'utf-8')

    return send_file(
                io.BytesIO(data),
                attachment_filename=route.downloadName,
#                mimetype='image/jpg'
        )


# From ChatGPT
def create_view_func(route):
    def view_func():
        return route.data
    return view_func


def create_view_func2(route):
    def view_func():
        # TODO necessary?
        data = route.data
        if isinstance(data, str):
            data = bytes(data, 'utf-8')

        ret = send_file(
            io.BytesIO(data),
            attachment_filename=route.downloadName,
#                mimetype='image/jpg'
        )
    
        return ret
    return view_func


def serve(routes: List[AceRoute]):
    """Start a webserver which serves the `routes`"""
    app = Flask(__name__)

    for route in routes:
        if isinstance(route.data, (AceStr, AceBytes)):
            print("Route: {}   Serving: {}    Donload: {} {}".format(route.url, route.data.index, route.download, route.downloadName))
        else:
            print("Route: {}   Donload: {} {}".format(route.url, route.download, route.downloadName))

        if route.download:
            app.add_url_rule(route.url, route.url, create_view_func2(route))
        else:
            app.add_url_rule(route.url, route.url, create_view_func(route))

    app.run()

