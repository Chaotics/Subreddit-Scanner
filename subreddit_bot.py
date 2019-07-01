class subredditBot():
    def createWrite(self, toWrite):
        raise NotImplementedError()
    def createRead(self, reddit):
        raise NotImplementedError()

    def backupWrite(self, reddit):
        raise NotImplementedError()
    def backupRead(self, reddit):
        raise NotImplementedError()

    def mimicWrite(self, toWrite):
        raise NotImplementedError()
    def mimicRead(self, toWrite):
        raise NotImplementedError()
    
