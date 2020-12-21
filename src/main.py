import json
import logging
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from telethon.sync import TelegramClient

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
telephone = os.getenv('TELEPHONE')
debug = bool(os.getenv('DEBUG'))
client = TelegramClient('alex', api_id, api_hash)


class Server(BaseHTTPRequestHandler):
    def _do_response(self, response_code):
        self.send_response(response_code)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("ok".encode("utf8"))

    def do_POST(self):
        post_data = self.rfile.read(int(self.headers['Content-Length']))
        if debug: logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))

        data = json.loads(post_data.decode('utf-8'))
        ping_id = client.send_message(data['username'], '/ping').id
        time.sleep(0.5)

        last_id = list(client.iter_messages(data['username'], limit=1))[0].id
        if debug: logging.info(
            str("ping_id = " + str(ping_id) + " last_id = " + str(last_id) + " difference = " + str(last_id - ping_id)))
        if last_id > ping_id:
            self._do_response(200)
        else:
            self._do_response(400)


def run(server_class=HTTPServer, handler_class=Server, port=8088):
    logging.basicConfig(level=logging.INFO)
    logging.info('start application')
    client.connect()
    client.start(phone=telephone)
    if debug: logging.info("connect to telegram")
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    if debug: logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    if debug: logging.info('Stopping httpd...\n')
    client.disconnect()


if __name__ == '__main__':
    run()
