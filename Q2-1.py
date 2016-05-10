# Q2-1.py

import http.server
import socketserver

httpd = socketserver.TCPServer(("", 8080),http.server.SimpleHTTPRequestHandler)

httpd.serve_forever()
