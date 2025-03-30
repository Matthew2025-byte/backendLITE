import network
import socket

class backendLITE:
    ap = None
    def __init__(self):
        pass
    
    def run(self, host="127.0.0.0", port=5000):
        addr = socket.getaddrinfo(host, port)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(1)
        print(f"Server running at {host}:{port}")

        html = """<!DOCTYPE html>
        <html>
            <head><title>Pico W Web Server</title></head>
            <body>
                <h1>Hello from your Pico W!</h1>
            </body>
        </html>
        """

        while True:
            try:
                conn, addr = s.accept()
                print('Connection from', addr)
                request = conn.recv(1024)
                print("Request:", request)

                conn.send('HTTP/1.1 200 OK\n')
                conn.send('Content-Type: text/html\n')
                conn.send('Connection: close\n\n')
                conn.sendall(html)
                conn.close()
            except Exception as e:
                print("Error:", e)

    
    def SendFile(self, filename):
        with open(filename, 'r') as file:
            content = file.read()
        return content
    
    def AccessPoint(self, SSID, Password):
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(essid=SSID, password=Password)

        self.run()
        self.ap.active(False)