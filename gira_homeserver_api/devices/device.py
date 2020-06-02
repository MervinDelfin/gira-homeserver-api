class Device:
    type = 1

    def setId(self, id):
        self.id = id
    
    def getId(self):
        return self.id

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name
    
    def setClient(self, client):
        self.client = client

    def getClient(self):
        return self.client

    def setValue(self, value):
        self.client.setDeviceValue(self.type, self.id, value)
    
    def getValue(self):
        return self.client.getDeviceValue(self.id)