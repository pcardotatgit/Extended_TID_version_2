'''
Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
'''
import http.server

PORT = 8888
server_address = ("localhost", PORT)

server = http.server.HTTPServer
handler = http.server.CGIHTTPRequestHandler

handler.cgi_directories = ["/cgi"]
print("Starting on port :", PORT)
print("Open your browser on http://localhost:8888")

httpd = server(server_address, handler)
httpd.serve_forever()