from .device import Device

class NormalizedDevice(Device):
    def setValue(self, value):
        if value >= 0 and value <= 1:
            super().setValue(round(value * 100))

    def getValue(self):
        return super().getValue() / 100