from .device import Device

class BinaryDevice(Device):
    def turnOn(self):
        self.setValue(1)
    
    def turnOff(self):
        self.setValue(0)

    def getState(self):
        return super().getValue() == 1.0
