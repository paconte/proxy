""" The proxy module

Implements a simple proxy with the configuration from the settings.py module
It do not use asyncronous programming
"""
import json
import socketserver
from http.server import BaseHTTPRequestHandler
import requests
import settings
import status
import jwttoken


proxy_host = settings.PROXY_HOST
proxy_port = settings.PROXY_PORT
proxy_endpoint = settings.PROXY_ENDPOINT
proxy_status_path = settings.PROXY_STATUS_PATH


def _get_jwt_header():
    jwt_token = jwttoken.get_default_jwt(
        key=settings.JWT_KEY,
        algo=settings.JWT_ALGO)
    return {settings.PROXY_JWT_HEADER: jwt_token}


def print_request(req):
    """methods for debugging purposes"""
    body = ""
    try:
        body = req.body
    except AttributeError:
        pass
    print('{}\n{}\n{}\n{}\n'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        'body: ' + str(body),
        '-----------END-------------'
    ))


def debug_request(method, url, json_data, headers):
    req = requests.Request(
        method, url, json=json_data, headers=headers).prepare()
    print_request(req)


class MyProxy(BaseHTTPRequestHandler):
    """This class is the handler of the http server"""

    def _set_get_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _set_post_response(self, resp):
        self.send_response(resp.status_code)
        headers = [
            'Content-Type',
            'Content-Length',
            'Access-Control-Allow-Origin']
        for key, val in resp.headers.items():
            if key in headers:
                self.send_header(key, val)
        self.end_headers()

    def _get_endpoint(self):
        return proxy_endpoint + self.path

    def _load_json(self):
        json_data = None
        value = self.headers.get('Content-Type', False)
        if 'json' in value:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            json_data = json.loads(post_data.decode('utf-8'))
        return json_data

    def _endpoints_headers(self, json_data):
        result = {}
        jwt = _get_jwt_header()
        result.update(jwt)
        if json_data is not None:
            result['Content-Type'] = 'application/json'
            result['Content-Length'] = self.headers['Content-Length']
        return result

    def do_GET(self):
        """HTTP GET action"""
        if proxy_status_path == self.path:
            self._set_get_response()
            post_requests = status.Status.requests()
            running_time = status.Status.running_str()
            self.wfile.write(
                "<h1>Running since: {}</h1><br/><h1>Requests: {}</h1>".format(
                    running_time, post_requests).encode('utf-8'))
        else:
            self.send_error(
                404,
                "Not Found",
                "Only the path {} is available".format(proxy_status_path))

    def do_POST(self):
        """HTTP POST action"""
        json_data = self._load_json()
        headers = self._endpoints_headers(json_data)
        url = self._get_endpoint()
        request = requests.post(url=url, json=json_data, headers=headers)
        debug_request('POST', url, json_data, headers)
        status.Status.increment()
        self._set_post_response(request)
        self.wfile.write(request.content)


def start_server(host, port):
    """"Method for stating the proxy server"""
    with socketserver.ForkingTCPServer((host, port), MyProxy) as httpd:
        print("\nstarting httpd on {}:{} ...\n".format(host, port))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        print("\nstopping httpd...\n")


if __name__ == '__main__':
    from sys import exit, argv

    if len(argv) == 2:
        arg_port = int(argv[1])
        if arg_port > 1024:
            proxy_port = int(argv[1])
        else:
            print("Invalid port number: {}".format(str(arg_port)))
            exit(1)
    elif len(argv) > 2:
        print("ERROR: Invalid arguments")
        print("Please use: python3 proxy.py [port=number] where number>1024")
        exit(1)

    start_server(proxy_host, proxy_port)
