import warnings
# to ignore all warnings
warnings.filterwarnings('ignore')

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import search
import os
import template_generator as t
import docx_generator
import os

host = '127.0.0.1'
port = 8000


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

            message = t.template_generator.template('template')
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


        if 'search' in form and 'id' in form:
            id = form['id'].value
            # get the user with the search module
            if search.find_user(id):
                data =  search.find_user(id)
                message = t.template_generator.template('template', data=data)
            else : 
                message = t.template_generator.template('template',message = 'khona wla khtna makayn(a)ch')  

        elif 'generate' in form:
            data_two = [None] * 8
            for i in range(8):
                data_two[i] = form[f'data_{i}'].value
            
            dg = docx_generator.docx_generator()
            dg.add_page_measurements()
            dg.add_heading()
            dg.add_title()
            dg.add_name(f'{data_two[1]} {data_two[2]}', f'{data_two[7][0].lower()}')
            dg.add_grade(data_two[3])
            dg.add_workplace(data_two[4])
            dg.add_rib(data_two[5])
            dg.add_bank(data_two[6])
            dg.add_agence(data_two[7],f'{data_two[7][0].lower()}')
            dg.end_of_file()

            doc = dg.doc

            path_doc = 'downloads/doc.docx'
            if os.path.exists(path_doc):
                os.remove(path_doc)
            doc.save(path_doc)

            try:
                os.startfile(r'downloads\doc.docx')
                message = t.template_generator.template('template',message = 'Done !')
            except FileNotFoundError as e:
                print(f'file not found in : {e.filename}')
            

            
        else:
            message = t.template_generator.template('template')


        self.wfile.write(bytes(message, 'utf8'))



# Function to start a server on a specific port
def start_server(port):
    with HTTPServer((host, port), handler) as server:
        print(f'server running in {host} with the port :{port}')
        server.serve_forever()



if __name__ == '__main__':
    start_server(port)
