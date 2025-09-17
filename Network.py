import network

class Network:
    wlan: network.WLAN
    ap: network.WLAN
    def __init__(self):
        pass

    def connect_to_wifi(self, SSID: str, Password: str) -> network.WLAN:
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(SSID, Password)

        while not self.wlan.isconnected():
            pass
        print(self.wlan.ifconfig())
        return self.wlan

    def AccessPoint(self, SSID: str, Password: str) -> network.WLAN:
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(essid=SSID, password=Password)
        print(f"Hosting access point: {SSID}")
        print(f"Password: {Password}")
        return self.ap
    
    def disconnect(self):
        try:
            self.wlan.disconnect()
            return True
        except:
            self.ap.disconnect()
            return True