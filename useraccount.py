

class User:
    def __init__(self):
        self.username = ''
        self.decryptkey = ''

    def login(self, username, password):
        pass

    def logout(self):
        return User()

    def getUser(self):
        return self.username
    
    def getDK(self):
        return self.decryptkey
    
    