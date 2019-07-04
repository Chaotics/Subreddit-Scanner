class subredditBot():
    def sendError(self, error):
        raise NotImplementedError()
    
    def createWrite(self, toWrite):
        raise NotImplementedError()
    def createRead(self, reddit):
        raise NotImplementedError()

    def backupWrite(self, toWrite):
        raise NotImplementedError()
    def backupRead(self, reddit):
        raise NotImplementedError()

    def mimicWrite(self, toWrite):
        raise NotImplementedError()
    def mimicRead(self, reddit):
        raise NotImplementedError()

    def saveWrite(self, toWrite):
        raise NotImplementedError()
    def saveRead(self, reddit):
        raise NotImplementedError()
    
