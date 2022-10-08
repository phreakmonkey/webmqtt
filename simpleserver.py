#!/usr/bin/env python3

__version__ = '0.9'

import http.server, select, signal, socket, socketserver, urllib.parse
import logging
import logging.handlers
import os
import sys
import urllib.request, urllib.error, urllib.parse

class TimeoutError(Exception):
  pass

def SIGALRM_handler(sig, stack):
  raise TimeoutError()

signal.signal(signal.SIGALRM, SIGALRM_handler)


class RequestHandler(http.server.BaseHTTPRequestHandler):
  __base = http.server.BaseHTTPRequestHandler
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

  def _safe(self, fname):
    if fname[0] == '.':
      return False
    safechars = ('abcdefghijklmnopqrstuvwxyz'
                 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                 '0123456789._- ')
    for x in fname:
      if x not in safechars:
        return False
    return True

  def do_GET(self):
    # Add additional files to serve here.
    # "URL" : "filename"
    routes = {
      '/': 'webmqtt.html',
      '/rssi': 'rssi.html',
      '/webint': 'webint.html',
      '/config.js': 'config.js',
    }

    if self.path in routes:
      fname = routes[self.path]
      with open(fname, 'rb') as hfile:
        content = hfile.read()
      self.send_response(200)
      if fname.endswith('.html'):
        self.send_header('Content-type', 'text/html')
      elif fname.endswith('.js'):
        self.send_header('Content-type', 'text/javascript')
      self.end_headers()
      self.wfile.write(content)
      return
    elif self.path.startswith('/firmware/'):
      fname = self.path.split('/')[2]
      if not fname or not self._safe(fname):
        self.send_error(418)
        return
      try:
        with open(f'firmware/{fname}', 'rb') as fw:
          content = fw.read()
      except FileNotFoundError:
          self.send_error(404)
          return
      self.send_response(200)
      self.send_header('Content-type', 'application/octet-stream')
      self.send_header('Content-length', str(len(content)))
      self.end_headers()
      self.wfile.write(content)
      return
    else:
      self._redirect("/")
      return

  do_POST = do_GET
  do_HEAD = do_GET
  do_PUT = do_GET


class ThreadingHTTPServer(socketserver.ThreadingMixIn,
                          http.server.HTTPServer):
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
