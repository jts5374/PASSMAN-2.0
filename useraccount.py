import encryption as enc
class User:
    def __init__(self):
        self.username = ''
        self.decryptkey = ''

    def login(self, username, password):
        self.username = username
        salt = enc.get_hashed_password_and_salt(username)[:29]
        dk = enc.generate_decrypt_key(password, salt)
        self.decryptkey = dk

    def logout(self):
        self.username = ''
        self.decryptkey = ''

    def getUser(self):
        return self.username
    
    def getDK(self):
        return self.decryptkey

    
    
    