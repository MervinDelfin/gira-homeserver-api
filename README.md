# Gira Homeserver API Client

Have access to all your GIRA home appliances.
You can turn lights on and off, open blinds via cronjobs or using a webfrontend (not included)
and open your garage when you come home (using flask + automate for Android).

**Only works with Python 3!**

# Table of contents

* [Installation](#installation)
* [Quick start](#quick-start-guide)
* [Device Types](#device-types)
* [Getting your devices](#how-do-i-get-the-device-ids)
* [Documentation of all functions](#all-functions)

## Installation

There are 3 ways of installating the API Client. We recommend using pip for smaller projects and requirements.txt for bigger ones.

### 1. pip (recommended)

Install using pip (**sometimes you have to use pip instead of pip3**)
```bash
pip3 install git+https://github.com/leoyn/gira-homeserver-api.git
```

### 2. pip + requirements.txt (for automated deployments)
If you are using a `requirements.txt` file you can the url as shown below:
```python
# other packages here
git@github.com:leoyn/gira-homeserver-api.git
```
Then do your `pip install -r requirements.txt`.

### 

### 3. manually (not recommended)
1. Clone using git: 
```bash
git clone git@github.com:leoyn/gira-homeserver-api.git
```
2. Copy `gira_homeserver_api.py` into your project folder 
```bash
cp gira-homeserver-api/gira_homeserver_api my-home-project/gira_homeserver_api
```

## Quick Start Guide

```python
import gira_homeserver_api as api

client = api.Client("127.0.0.1", 80, "username", "password")

# listener when client is ready, because connect() blocks thread
def onClientReady(sessionToken):
    type = 1
    id = 101
    value = 1
    # Turn device 101 on
    client.setDeviceValue(type, id, value)

client.onClientReady(onClientReadyListener)

# connnect and block thread
client.connect()
```

For more in depth comments check out the example.py

**What is this code doing?**

It connects to your homeserver with the given credentials and turns on a lamp with id 101.

## Device Types


|Type| Description | Example devices|
|----|-------------|----------------|
| 0  | Used to get a value from a device instead of setting one | All devices
| 1  | Set device value | Lights, Blinds, Thermostats
| 20 | Also set device value. The only type that works with a garage | Garage


## How do I get the device IDs?

1. Download your device list

```python
import gira_homeserver_api as api

client = api.Client("127.0.0.1", 80, "username", "password")

def onClientReady(sessionToken):
    # open file and download devices
    file = open("my_devices.xml", "w")
    file.write(client.getDevices())
    file.close()
    # close connection
    client.close()


client.onClientReady(onClientReady)
client.connect()
```


2. Open the file `my_devices.xml` with a text editor and search for devices. Example:
```xml
<device id="200" txt="House\Basement\Room\Socket" template="0-16_5" uhr="1000000010">
    <connect slot="slot_bin" tag="1337" />
</device>
```

**`1337` IS the device id and NOT `200`. TAG = Device Id**

3. Control your socket by the api
```python
import gira_homeserver_api as api

client = api.Client("127.0.0.1", 80, "username", "password")

def onClientReady(sessionToken):
    # turns your socket with id 1337 on
    client.setDeviceValue(1, 1337, 1)

client.onClientReady(onClientReady)
client.connect()
```


## All functions

Please create an object first!

```python
client = api.Client("127.0.0.1", 80, "username", "password")
```

List of all function the api exposes:

### setDeviceValue(deviceType, deviceId, value)

```python
client.setDeviceValue(1, 101, 1)
```

### Deprecated ~~setDevice(deviceType, deviceId, value)~~

Please use [`setDeviceValue(deviceType, deviceId, value)`](#setdevicevaluedevicetype-deviceid-value) instead

### getDeviceValue(deviceId): float

Returns always a float value from device with given id. Returns `-1` when device does not respond

```python
value = client.getDeviceValue(101)
```


### onDeviceValue(listener)

Listens for all device value changes

```python
def onDeviceValueListener(deviceId, value):
    print(deviceId, value)

client.onDeviceValue(onDeviceValueListener)
```


### connect()

Connect to homeserver. Blocks thread.\
Must be called **after setting listeners** and **before get or setting values** of devices.

```python
client.connect()
```

### onClientReady(listener)

It is recommended to execute sets and gets of device values after onClientReady listener received the ready event

```python
def onClientReadyListener():
    print("Client is ready")
    client.setDeviceValue(1, 101, 1)
    print("Device value is", client.getDeviceValue(101))

client.onClientReady(onClientReadyListener)
```

### onConnectionError(listener)

Listens for connection error

```python
def onConnectionErrorListener():
    print("Client connection aborted")

client.onConnectionError(onConnectionErrorListener)
```
