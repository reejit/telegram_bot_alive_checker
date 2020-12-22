import json
import logging
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from telethon.sync import TelegramClient


def str2bool(boolean_string):
    return boolean_string.lower() in ("yes", "true", "t", "1")


api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
telephone = os.getenv('TELEPHONE')
debug = str2bool(os.getenv('DEBUG'))
client = TelegramClient('alex', api_id, api_hash)


class Server(BaseHTTPRequestHandler):
    def _do_response(self, response_code):
        self.send_response(response_code)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("ok".encode("utf8"))

    def do_POST(self):
        post_data = self.rfile.read(int(self.headers['Content-Length']))
        if debug:
            logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                         str(self.path), str(self.headers), post_data.decode('utf-8'))

        data = json.loads(post_data.decode('utf-8'))
        ping_id = client.send_message(data['username'], '/ping').id
        time.sleep(0.5)

        messages_after_ping = list(client.iter_messages(data['username'], min_id=ping_id))

        logging.info(data['username'])
        if debug:
            logging.info("ping_id = %s count of message after it = %s", str(ping_id), len(messages_after_ping))

        if len(messages_after_ping) > 0:
            self._do_response(200)
        else:
            self._do_response(400)


def run():
    logging.info('start application')

    client.connect()
    client.start(phone=telephone)

    if debug:
        logging.info("connect to telegram")

    server_address = ('', 8088)
    httpd = HTTPServer(server_address, Server)

    if debug:
        logging.info('Starting httpd...\n')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

    if debug:
        logging.info('Stopping httpd...\n')

    client.disconnect()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
