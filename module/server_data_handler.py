import warnings

# to ignore all warnings
warnings.filterwarnings('ignore')

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import search

class handler(BaseHTTPRequestHandler):

    # description of how to handle GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = 'salam Youssef'
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
                message = f'Hello, {data[1]} {data[2]}'
            else : 
                message = 'khona wla khtna makayn(a)ch'
        else:
            message = 'ma Hellowch asidi'

        self.wfile.write(bytes(message, 'utf8'))

host = '127.0.0.1'
port = 8000
if __name__ == '__main__':
    with HTTPServer((host, port), handler) as server:
        print(f'server running in {host} with the port :{port}')
        server.serve_forever()