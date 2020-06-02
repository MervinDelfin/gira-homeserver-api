# Gira Homeserver API Client

Have access to all your GIRA home appliances.
You can turn lights on and off, open blinds via cronjobs or using a webfrontend (not included)
and open your garage when you come home (using flask + automate for Android).

**Only works with Python 3!**

# Table of contents

* [Installation](#installation)
* [Quick start](#quick-start-guide)
* [Internal Device Types](#internal-device-types)
* [Getting your devices](#how-do-i-get-the-device-ids)
* [Documentation](#documentation)
  * [Client](#client)
  * [Parser](#parser)
  * [Devices](#devices)

## Installation

There are 3 ways of installing the API Client. We recommend using pip for smaller projects and requirements.txt for bigger ones.

### 1. pip (recommended)

Install using pip (**sometimes you have to use pip instead of pip3**)
```bash
pip3 install git+https://github.com/leoyn/gira-homeserver-api.git
```

### 2. pip + requirements.txt (for automated deployments)
If you are using a `requirements.txt` file you can add the URL as shown below:
```python
# other packages here
git+https://github.com/leoyn/gira-homeserver-api.git
```
Then do your `pip3 install -r requirements.txt`.

### 

### 3. manually (not recommended)
1. Clone using git: 
```bash
git clone git@github.com:leoyn/gira-homeserver-api.git
```
2. Copy the `gira_homeserver_api` folder into your project folder
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

For more in depth comments check out the [quick_start.py](https://github.com/leoyn/gira-homeserver-api/blob/master/examples/quick_start.py) in the examples directory.

**What is this code doing?**

It connects to your homeserver with the given credentials and turns on a lamp with id 101.

## Internal Device Types

These are device types when you access your Gira Homeserver directly via the client.
When you want to use the device object instead look for [here](#devices).
They use the same devices types of GIRA but asbtract the numerical types by providing appropiate functions.

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


## Documentation

* [Client](#client)
* [Parser](#parser)
* [Devices](#devices)

### Client

```python
client = api.Client("127.0.0.1", 80, "username", "password")
```

#### setDeviceValue(deviceType, deviceId, value)

```python
client.setDeviceValue(1, 101, 1)
```

#### Deprecated ~~setDevice(deviceType, deviceId, value)~~

Please use [`setDeviceValue(deviceType, deviceId, value)`](#setdevicevaluedevicetype-deviceid-value) instead

#### getDeviceValue(deviceId): float

Always returns a float value for device with given id.\
Returns `None` when device does not respond or device does not exist.

```python
value = client.getDeviceValue(101)
```


#### onDeviceValue(listener)

Listens for all device value changes

```python
def onDeviceValueListener(deviceId, value):
    print(deviceId, value)

client.onDeviceValue(onDeviceValueListener)
```


#### connect()

Connect to homeserver.\
Must be called **after setting listeners** and **before get or setting values** of devices.

```python
client.connect()
```

**Arguments:**
* `asynchronous`: When setting to `True` client won't block thread. Default: `False`.
* `reconnect`: automatically reconnect when connections drops. Default: `True`.

#### onClientReady(listener)

It is recommended to execute sets and gets of device values after onClientReady listener received the ready event

```python
def onClientReadyListener():
    print("Client is ready")
    client.setDeviceValue(1, 101, 1)
    print("Device value is", client.getDeviceValue(101))

client.onClientReady(onClientReadyListener)
```

#### onConnectionError(listener)

Listens for connection error

```python
def onConnectionErrorListener():
    print("Client connection aborted")

client.onConnectionError(onConnectionErrorListener)
```

#### close()

Close connection

```python
client.close()
```

#### send(text)

Send raw text to server.\
**Please be aware that this might has negative side effects. Use with caution.**

```python
client.send("1|1|1")
```

### Parser

You can find an example in the [using_the_device_parser.py](https://github.com/leoyn/gira-homeserver-api/blob/master/examples/using_the_device_parser.py) in the example directory.

```python
devices = api.Parser.parse(client.getDevices(), client)
```

Note: `client` (2nd argument) is optional. If you don't provide it, devices cannot be controlled.

### Devices

All devices have the following methods:

* `getId()` : get gevice ID
* `setId(id)` : set device ID
* `getValue()`: get value of device
* `setValue(id)`: set value of device
* `getName()`: get name. e.g. `floor\area\room\object`
* `setName(id)`: set name
* `getClient()`: get [client](#client) object
* `setClient(client)`: set [client](#client) object

#### Binary Device

Has only two states: `on` or `off`.

* `turnOn()`: turns device on
* `turnOff()`: turns device off
* `getState()`: returns `True` = on **or** `False` = off

#### NormalizedDevice

Will set a device value on a scale from 0 to 1.

0 = 0% \
1 = 100%

* `setValue(value)`: set device value between 0 and 1
* `getValue()`: get device value

#### SequenceValue

Acts as a normal device. However it has `20` as the [internal device type](#internal-device-types).


#### ValueDevice

Value devices take any arbitrary input you give it. Basically the same as sequence device with the internal device type `1`.
