import socket
from .Response import Response
# Also uses micropython network and ujson modules


class backendLITE:
    """
    Testing on Pico W has not yet been performed.
    
    conn.recv(1024) on line 27 may have to be lowered
    """
    
    server_handlers = {}

    def __init__(self):
        pass

    def run(self, host="127.0.0.1", port=5000):
        addr = (host, port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(addr)
        s.listen(1)
        print(f"Server running at {host}:{port}")

        while True:
            try:
                conn, addr = s.accept()
                request = conn.recv(1024).decode('utf-8')
                if not self.ValidRequest(request):
                    conn.close()
                    continue
                method, route, protocol = request.splitlines()[0].split(" ")

                response, headers = self.HandleRoute(route)

                print(f'{method} "{route}" {headers["status"]}')

                Response.SendAndClose(conn, response, headers)
            except Exception as e:
                print(f"Error: {e}")

    @staticmethod
    def ValidRequest(request):
        if not request.strip():
            print("Invalid Request: ", request.strip())
            return False
        if not request.splitlines():
            return False
        return True
        
    @staticmethod
    def send_file(filename):
        try:
            with open(filename, 'r') as file:
                content = file.read()
            return content, {"Content-Type": Response.GuessMimeType(filename)}
        except FileNotFoundError:
            return "<h1>404 File Not Found</h1>", {'status': 404, 'Content-Type': 'text/html'}

    def add_route(self, path, func):
        self.server_handlers[path] = func


    def HandleRoute(self, route):
        if route not in self.server_handlers:
            return "<h1>404 Not Found</h1>", {'status': 404, 'Content-Type': "text/html"}
        
        response = self.server_handlers[route]()

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
    

    def Connect_to_Wifi(self, SSID, Password):
        import network
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(SSID, Password)

    def AccessPoint(self, SSID, Password):
        import network
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid=SSID, password=Password)
        print(f"Hosting access point: {SSID}")
        print(f"Password: {Password}")



def jsonify(data):
    import ujson
    return ujson.dumps(data), {"Content-Type": "application/json"}