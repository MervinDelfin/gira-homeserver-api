# Gira Homeserver API

Git clone or download api.py. Only works **with Python 3!**

## How do I use it?

Put the api.py in your project folder

```
import api

client = api.Client("127.0.0.1", 80, "username", "password")

# listener when client is ready, because connect() blocks thread
def onClientReadyListener():
    type = 1
    id = 101
    value = 1
    # Turn device 101 on
    client.setDevice(type, id, value)

client.onClientReady(onClientReadyListener)

# connnect and block thread
client.connect()
```

For more in depth comments check out the example.py

**What is the code doing?**

It connects to your homeserver with the given credentials and turns on a lamp with id 101.

## Device Types


|Type| Description | Example devices|
|----|-------------|----------------|
| 0  | Used to get a value from a device instead of setting one | All devices
| 1  | Set device value | Lights, Blinds, Thermostats
| 20 | Also set device value. The only type that works with a garage | Garage


## More functions of Client class

Please create an object first!
```
client = api.Client("127.0.0.1", 80, "username", "password")
```

List of all function the api exposes:

### setDevice(deviceType, deviceId, value)

```
client.setDevice(1, 101, 1)
```


### getDeviceValue(deviceId): float

Returns always a float value from device with given id. Returns `-1` when device does not respond

```
value = client.getDeviceValue(101)
```


### onDeviceValue(listener)

Listens for all device value changes

```
def onDeviceValueListener(deviceId, value):
    print(deviceId, value)

client.onDeviceValue(onDeviceValueListener)
```


### connect()

Connect to homeserver. Blocks thread.\
Must be called **after setting listeners** and **before get or setting values** of devices.

```
client.connect()
```

### onClientReady(listener)

It is recommended to execute sets and gets of device values after onClientReady listener received the ready event

```
def onClientReadyListener():
    print("Client is ready")
    client.setDevice(1, 101, 1)
    print("Device value is", client.getDeviceValue(101))

client.onClientReady(onClientReadyListener)
```

### onConnectionError(listener)

Listens for connection error

```
def onConnectionErrorListener():
    print("Client connection aborted")

client.onConnectionError(onConnectionErrorListener)
```
