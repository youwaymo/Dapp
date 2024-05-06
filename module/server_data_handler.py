import warnings
# to ignore all warnings
warnings.filterwarnings('ignore')

# import the needed modules from jinja2
from jinja2 import Environment, FileSystemLoader, select_autoescape

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import search
import os
import template


class handler(BaseHTTPRequestHandler):

    # description of how to handle GET requests
    def do_GET(self):
        if self.path.endswith(('.css', '.js', '.png', '.woff2', '.ttf')):
            # Serving CSS, JS, webfonts and image files
            # os.path.splitext() splits the pathname self.path into a tuple (root, extention)
            file_extension = os.path.splitext(self.path)[1]

            # get the content type of the file being sent otherwise send 'application/octet-stream' 
            # that it means to send an unkonwn file type to the browser and tell it not interpret it
            content_type = {
                '.css': 'text/css',
                '.js': 'text/javascript',
                '.png': 'image/png',
                '.woff2': 'font/woff2',
                '.ttf': 'font/ttf'
            }.get(file_extension, 'application/octet-stream')

            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()

            try:
                with open('.' + self.path, 'rb') as file:
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_error(404, f'File Not Found: {self.path}')

        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            tmplt = template.template_generator.template('template')
            message = tmplt.render()

            self.wfile.write(bytes(message, 'utf8'))
    
    # description of how to handle POST requests
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # to parse the data sent from the form 
        form = cgi.FieldStorage(
            fp=self.rfile, # it gets the binary data sent by the form and then it read it
            headers=self.headers, # gets the header
            environ={'REQUEST_METHOD': 'POST'} # inform the cgi with request method
        )
        
        if 'id' in form:
            id = form['id'].value
            # get the user with the search module
            if search.find_user(id):
                data =  search.find_user(id)
                message = template('template').render(data = data)

            else : 
                message = template('template').render(message = 'khona wla khtna makayn(a)ch')
        else:
            message = template('template').render(message = 'rak ma9lbti 3la walo')

        self.wfile.write(bytes(message, 'utf8'))

host = '127.0.0.1'
port = 8000
if __name__ == '__main__':
    with HTTPServer((host, port), handler) as server:
        print(f'server running in {host} with the port :{port}')
        server.serve_forever()
