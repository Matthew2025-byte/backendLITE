import socket
import json
from .Response import Response
from .Response import Request
# Also uses micropython network and ujson modules


class backendLITE:
    """
    Testing on Pico W has not yet been performed.
    
    conn.recv(1024) on line 27 may have to be lowered
    """
    
    server_handlers = {}
    _static_directory = "/static"

    def __init__(self):
        pass

    def run(self, host: str="127.0.0.1", port: int=5000):
        addr = (host, port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(addr)
        s.listen(1)
        print(f"Server running at {host}:{port}")

        while True:
            try:
                conn, addr = s.accept()
                request = Request(conn.recv(1024).decode('utf-8'))
                print(f'{request.method} "{request.route}"')

                response, headers = self.HandleRoute(request)

                Response.SendAndClose(conn, response, headers)
            except Exception as e:
                print(f"Error: {e}")

                
        
    @staticmethod
    def send_file(filename: str):
        try:
            with open(filename, 'r') as file:
                content = file.read()
            return content, {"Content-Type": Response.GuessMimeType(filename)}
        except:
            return "<h1>404 File Not Found</h1>", {'status': 404, 'Content-Type': 'text/html'}

    def route(self, path):
        def wrapper(func):
            self.add_route(path, func)
        return wrapper

    def add_route(self, path: str, func):
        self.server_handlers[path] = func

    def staticdir(self, path):
        self._static_directory = path

    def HandleRoute(self, request: Request):
        method = request.method
        route = request.route

        if self._static_directory in route:
            return self.Response_Headers(self.send_file(route[1:]))

        if route not in self.server_handlers:
            return "<h1>404 Not Found</h1>", {'status': 404, 'Content-Type': "text/html"}
        
    
        handler = self.server_handlers[route]
        if "request" in handler.__code__.co_varnames[:handler.__code__.co_argcount]:
            response = handler(request)
        else:
            response = handler()
        
        
        response, headers = self.Response_Headers(response)

        return response, headers

        
    @staticmethod
    def Response_Headers(response):
        if isinstance(response, tuple): # Checks if user function returned tuple
            response, headers = response

            if not isinstance(headers, dict): # checks if user only set a status code (e.g. return "response", 200)
                headers = {"status": headers}

            if isinstance(response, tuple): # checks if user returned a function output which contained headers
                response, additional_headers = response

                for key, value in additional_headers.items():
                    headers[key] = value
            
            if "status" not in headers or headers["status"] == None:
                headers["status"] = 200
            if "Content-Type" not in headers or headers["Content-Type"] == None:
                headers["Content-Type"] = "text/html"
        else:
            headers = {"Content-Type": "text/html", "status": 200}

        return response, headers
    

    

    



def jsonify(data):
    return json.dumps(data), {"Content-Type": "application/json"}

def render_template(file_location, **kwargs):
    if not file_location.endswith(".html"):
        raise Exception("render_template must use an HTML file")
    try:
        with open(file_location) as file:
            template = str(file.read())

            for key, value in kwargs.items():
                template = template.replace(f"{{{{{key}}}}}", value)
            return template, {"Content-Type": "text/html", "status": 200}
    except FileNotFoundError:
        return "<h1>404 Not Found</h1>", {"Content-Type": "text/html", "status": 404}