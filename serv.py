#!/usr/bin/python
import sys
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from habrpars import HabrPars

HOST = 'http://127.0.0.1'
PORT = 8086
main_page = ['/?utm_source=tm_habrahabr&utm_medium=tm_top_panel&utm_campaign='
             'tm_promo', '/']


class HabrServ(BaseHTTPRequestHandler):

    def set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        return message.encode("utf8")

    def do_HEAD(self):
        self.set_headers()

    def do_GET(self):
        if self.path in main_page:
            self.send_response(301)
            new_path = f'{HOST}:{PORT}/ru/'
            self.send_header('Location', new_path)
            self.end_headers()
        else:
            self.set_headers()
            self.wfile.write(HabrPars().get_text(f'{HOST}:{PORT}', self.path))

    def log_message(self, format, *args):
        sys.stderr.write(f'{self.address_string()}::{PORT} - - '
                         f'{self.log_date_time_string()} - - {format%args}\n')

    @staticmethod
    def run():
        serv = HTTPServer(('', PORT), HabrServ)
        try:
            print(f'----Starting http server--at--{time.ctime()}---')
            serv.serve_forever()
        except KeyboardInterrupt:
            print(f'----Stopping http server--at--{time.ctime()}--')
            serv.socket.close()

