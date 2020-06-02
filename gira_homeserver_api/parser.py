from .devices.normalized_device import NormalizedDevice
from .devices.binary_device import BinaryDevice
from .devices.value_device import ValueDevice
from .devices.sequence_device import SequenceDevice

import xml.etree.ElementTree as ElementTree

class Parser:
    @staticmethod
    def parse(text, client = None):
        root = ElementTree.fromstring(text)
        xmlDevices = root.find("devices")

        devices = []

        for xmlDevice in xmlDevices.findall("device"):
            for xmlConnect in xmlDevice.findall("connect"):
                device = None
                
                if xmlConnect.attrib["slot"] == "dim_val" or xmlConnect.attrib["slot"] == "jal_val_write":
                    device = NormalizedDevice()
                elif xmlConnect.attrib["slot"] == "slot_bin":
                    device = BinaryDevice()
                elif xmlConnect.attrib["slot"] == "temp_soll":
                    device = ValueDevice()
                elif xmlConnect.attrib["slot"] == "seq_val":
                    device = SequenceDevice()

                if device != None:
                    device.setName(xmlDevice.attrib["txt"])

                    if isinstance(device, SequenceDevice):
                        device.setId(xmlConnect.attrib["id"])
                    else:
                        device.setId(int(xmlConnect.attrib["tag"]))
                    
                    device.setClient(client)

                    devices.append(device)
                    break
        return devices
