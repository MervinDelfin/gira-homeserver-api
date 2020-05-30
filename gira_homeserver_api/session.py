class Session:
    def __init__(self, sessionToken):
        self.sessionToken = sessionToken

    def getSessionToken(self):
        return self.sessionToken