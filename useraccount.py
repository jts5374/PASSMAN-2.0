import encryption as enc
import sql
class User:
    def __init__(self):
        self.username = ''
        self.decryptkey = ''

    def login(self, username, password, qpassword):
        self.username = username
        salt = qpassword[:29]
        dk = enc.generate_decrypt_key(password, salt)
        self.decryptkey = dk

    def logout(self):
        self.username = ''
        self.decryptkey = ''

    def getUser(self):
        return self.username
    
    def getDK(self):
        return self.decryptkey

    
    
    