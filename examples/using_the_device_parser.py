import gira_homeserver_api as api
import time

client = api.Client("XXX.XXX.XXX", 80, "username", "password")

def clientReady(sessionKey):
    # parse devices
    devices = api.Parser.parse(client.getDevices(), client)
    for device in devices:
        # control the one with id 101
        if device.getId() == 101:
            print(device.getType(), device.getName())
            device.setValue(0.5)
    
    # take a 5s nap
    time.sleep(5)

    # create a device manually
    device = api.NormalizedDevice()
    device.setId(1552)

    # IMPORTANT: Do this or you won't be able to control your device
    device.setClient(client)
    device.setValue(1)

    # Check if it worked
    print(device.getValue())

    # bye
    client.close()
    

client.onClientReady(clientReady)
client.connect()