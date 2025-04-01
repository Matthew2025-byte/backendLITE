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

    def __init__(self, method: str):
        self.method = method
    