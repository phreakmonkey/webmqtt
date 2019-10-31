#!/usr/bin/python

__version__ = '0.1'

import BaseHTTPServer, select, signal, socket, SocketServer, urlparse
import logging
import logging.handlers
import os
import sys
import urllib2

class TimeoutError(Exception):
  pass

def SIGALRM_handler(sig, stack):
  raise TimeoutError()

signal.signal(signal.SIGALRM, SIGALRM_handler)


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  __base = BaseHTTPServer.BaseHTTPRequestHandler
  __base_handle = __base.handle
  server_version = "HTTPHandler/" + __version__

  def log_message(self, format, *args):
    logging.info('%s ' + format, self.client_address[0], *args)
    return

  def handle(self):
    (ip, port) =  self.client_address
    if hasattr(self, 'allowed_clients') and ip not in self.allowed_clients:
      self.raw_requestline = self.rfile.readline()
      if self.parse_request(): self.send_error(403)
    else:
      self.__base_handle()

  def _redirect(self, location):
    self.send_response(307)
    self.send_header('Location', location)
    self.end_headers()

  def do_GET(self):
    if self.path == '/':                             
      with open('webmqtt.html', 'r') as hfile:
        content = hfile.read()
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()
      self.wfile.write(content)
      return

    self._redirect("/")

  do_POST = do_GET
  do_HEAD = do_GET
  do_PUT = do_GET


class ThreadingHTTPServer(SocketServer.ThreadingMixIn,
                          BaseHTTPServer.HTTPServer):
  pass


def main():
  FORMAT = 'simpleserver: %(message)s'
  logging.basicConfig(format=FORMAT, level=getattr(logging, 'INFO'))
  logger = logging.getLogger()
  handler = logging.handlers.SysLogHandler(address='/dev/log',
      facility='local3')
  formatter = logging.Formatter(fmt=FORMAT)
  handler.setFormatter(formatter)
  logger.addHandler(handler)
  #if os.fork():
  #  sys.exit()
  server = ThreadingHTTPServer(('', int(sys.argv[1])), RequestHandler)
  server.serve_forever()


if __name__ == '__main__':
  main()
