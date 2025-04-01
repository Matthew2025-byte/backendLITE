class Response:
    @staticmethod
    def SendHeaders(conn, headers):
        conn.send(f'HTTP/1.1 {headers["status"]}\r\n'.encode()) # Start headers

        for key, value in headers.items(): # Send headers

            conn.send(f"{key}: {value}\r\n".encode())

        conn.send('Connection: close\r\n\r\n'.encode()) # Close connection
    
    @staticmethod
    def SendAndClose(conn, content, headers):
        Response.SendHeaders(conn, headers)
        conn.sendall(content.encode())
        conn.close()
    
    @staticmethod
    def GuessMimeType(filename):
        if filename.endswith('.html'):
            return 'text/html'
        elif filename.endswith('.css'):
            return 'text/css'
        elif filename.endswith('.js'):
            return 'application/javascript'
        elif filename.endswith('.png'):
            return 'image/png'
        elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
            return 'image/jpeg'
        elif filename.endswith('.gif'):
            return 'image/gif'
        else:
            return 'application/octet-stream'
        

class Request:
    method: str
    route: str

    request_headers: str
    request_body: str
    

    def __init__(self, request_message: str):
        self.method, self.route, _ = request_message.splitlines()[0].split(" ")
        self.request_headers, self.request_body = request_message.split("\r\n\r\n", 1)


    def form(self):
        items = self.request_body.split("&")
        form = {}
        for item in items:
            key, value = item.split("=")
            form[key] = value
        return form
