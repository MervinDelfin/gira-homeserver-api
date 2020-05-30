import _thread
import socket
import hashlib
import urllib.request
from time import sleep, time
from .session import Session

STATE_NOT_CONNECTED = 0
STATE_CONNECTED = 1
STATE_LOGGED_IN = 2

CONNECTION_ERROR_TIMED_OUT = 1
CONNECTION_ERROR_REFUSED = 2


class Client:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = int(port)
        self.username = username
        self.password = password

        self.__eventListeners = {
            "deviceValueBroadcast": [],
            "deviceValue": {},
            "ready": [],
            "error": []
        }

        self.state = STATE_NOT_CONNECTED

    def connect(self, timeout = 30.0, asynchronous = False):
        if asynchronous == True:
            _thread.start_new_thread(self.__connect,(timeout,))
        else:
            self.__connect(timeout)

    def __connect(self, timeout):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.settimeout(timeout)
            self.__socket.connect((self.host, self.port))

            self.state = STATE_CONNECTED

            try:
                self.__connection = self.__listener(self.username, self.password)
            except KeyboardInterrupt:
                exit(0)
        except OSError:
            for handler in self.__eventListeners["error"]:
                handler(CONNECTION_ERROR_TIMED_OUT)

            return CONNECTION_ERROR_TIMED_OUT
        except ConnectionRefusedError:
            for handler in self.__eventListeners["error"]:
                handler(CONNECTION_ERROR_REFUSED)

            return CONNECTION_ERROR_REFUSED

    def __listener(self, username, password):
        # start login procedure
        self.__socket.sendall(("GET /QUAD/LOGIN \r\n\r\n").encode())

        while True: 
            data = self.__socket.recv(2048)

            if data:
                data = data.decode()
                args = data.split("|")
                try:
                    action = int(args[0])
                except:
                    raise Exception("Wrong data from server")
                    exit(0)
                else:
                    if action == 100:
                        # provide username
                        self.__send("90|" + username + "|")
                    elif action == 91:
                        # provide hashed password
                        self.__send("92|" + self.__generateHash(username, password, args[1]) + "|")
                    elif action == 93:
                        # login succeeded
                        self.state = STATE_LOGGED_IN
                        self.session = Session(args[1])

                        for handler in self.__eventListeners["ready"]:
                            _thread.start_new_thread(handler, (args[1],))

                    elif action == 1:
                        for i in range(0,int((len(args)-1)/3)):
                            for handler in self.__eventListeners["deviceValueBroadcast"]:
                                _thread.start_new_thread(handler, (int(args[1 + i * 3]), float(args[2 + i * 3])))

                            if args[1] in self.__eventListeners["deviceValue"]:
                                self.__eventListeners["deviceValue"][str(args[1 + i * 3])] = float(args[2 + i * 3])
            else:
                break
        

    def getDeviceValue(self, id):
        self.__eventListeners["deviceValue"][str(id)] = -1
        self.__send("2|" + str(id) + "|0")

        start = time()

        while self.__eventListeners["deviceValue"][str(id)] == -1 and time() - start < 2:
            sleep(0.1)

        value = self.__eventListeners["deviceValue"][str(id)]

        del self.__eventListeners["deviceValue"][str(id)]

        return value

    def onConnectionError(self, handler):
        self.__eventListeners["error"].append(handler)

    def onClientReady(self, handler):
        self.__eventListeners["ready"].append(handler)

    def onDeviceValue(self, handler):
        self.__eventListeners["deviceValueBroadcast"].append(handler)

    def send(self, message):
        self.__send(message)

    def __send(self, message):
        self.__socket.sendall((str(message) + "\x00").encode())

    def setDeviceValue(self, type, id, value = 0):
        if self.state == STATE_LOGGED_IN:
            self.__send(str(int(type)) + "|" + str(id) + "|" + str(value))
        else:
            raise Exception("Not logged in. Please connect and login first before controlling devices.")

    def setDevice(self, type, id, value = 0):
        self.setDeviceValue(type, id, value)

    def getDevices(self, sessionToken = None):
        
        if self.state == STATE_LOGGED_IN or sessionToken is not None:

            if sessionToken is None:
                sessionToken = self.session.getSessionToken()

            with urllib.request.urlopen(f"http://{self.host}:{self.port}/quad/client/client_project.xml?{sessionToken}") as handle:
                return handle.read().decode("utf-8")
        else:
            raise Exception("Please provide a sessionToken as argument or login first")

    def __generateHash(self, username, password, salt):
        salt = [ord(c) for c in salt]
        arr1 = [salt[i] ^ 92 if len(salt) > i else 92 for i in range(64)]
        arr2 = [salt[i] ^ 54 if len(salt) > i else 54 for i in range(64)]
        arr1 = "".join([chr(b) for b in arr1])
        arr2 = "".join([chr(b) for b in arr2])
        hash = hashlib.md5((arr2 + username + password).encode()).hexdigest().upper()
        hash = hashlib.md5((arr1 + hash).encode()).hexdigest().upper()
        return hash

    def close(self):
        if self.state != STATE_NOT_CONNECTED:
            self.__socket.close()
            self.state = STATE_NOT_CONNECTED
