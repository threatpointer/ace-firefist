from flask import Flask, send_file
import io
from urllib.parse import urlparse
import os

# a View which just returns `data`
def serveData(route):
    return f"{route.data}"


def serveDownload(route):
    #filename = os.path.basename(urlparse(route.url).path)

    return send_file(
                io.BytesIO(route.data),
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
        return send_file(
            io.BytesIO(route.data),
            attachment_filename=route.downloadName,
#                mimetype='image/jpg'
        )
    return view_func


def serve(routes):
    """Start a webserver which serves the `routes`"""
    app = Flask(__name__)

    for route in routes:
        if route.download:
            app.add_url_rule(route.url, route.url, create_view_func2(route))
        else:
            app.add_url_rule(route.url, route.url, create_view_func(route))

    app.run()

