import sqlite3 
import os

class Database:
    def __init__(self) -> None:
        self.dbpath = os.path.dirname(os.path.realpath(__file__))
        self.setConnection()
        

    def getPath(self):
        return self.dbpath

    def setPath(self, newpath):
        self.dbpath = newpath
        self.initialize_db()
        self.setConnection()

    def setConnection(self):
        self.con = sqlite3.connect(os.path.join(self.dbpath, 'passMan.db'))
        self.cur = self.con.cursor()

    def initialize_db(self):        
        self.cur.execute("""
        create table if not exists accounts(   
            UserName varchar(255) Primary Key ,
            MasterPassword varchar(255))
        """)

        self.cur.execute("""
        create table if not exists userpasswords(   
            AccountEntry integer Primary Key,
            Site varchar(255),
            SiteUserName varchar(255),
            Password varchar(255),
            MasterUserName varchar(255),
            Foreign Key (MasterUserName) References accounts(UserName)
            )
        """)
        self.con.commit()

    #---------Inserts----------------
    def insertNewUser(self, username, hashedpw):
        self.cur.execute("""
        INSERT INTO ACCOUNTS (UserName, MasterPassword)
        VALUES (? , ?)
        """, (username, hashedpw))
        self.con.commit()

    def insertIntoUserPasswords(self,masterusername, site= '',siteusername = '', password = '' ):
        self.cur.execute("""
        INSERT INTO USERPASSWORDS(Site, SiteUserName, Password, MasterUserName)
        VALUES(?,?,?,?)
        """, (site, siteusername, password, masterusername,))

        self.con.commit()
    #---------Delete-------------------
    def deleteUserAccount(self, username):
        self.cur.execute("""
        DELETE FROM Accounts
        WHERE UserName = ?
        """, (username,))
        self.cur.execute("""
        DELETE FROM userpasswords
        WHERE MasterUserName = ?
        """, (username,))
        self.con.commit()

    def deleteUserPasswordsSite(self, idx):
        self.cur.execute("""
        DELETE FROM userpasswords
        WHERE AccountEntry = ?
        """, (idx, ))

    #------------Retrieve-----------------
    def selectPassword(self, username):
        query = self.cur.execute("""
        SELECT MasterPassword
        FROM Accounts
        WHERE UserName = ? 
        """,(username, ))
        return query.fetchone()[0]

    def selectuserPasswordsData(self, username):
        query = self.cur.execute("""
        SELECT * 
        FROM userpasswords
        WHERE MasterUserName = ?
        """, (username,))
        return query.fetchall()

    def getMasterAccount(self, username):
        query = self.cur.execute("""
        SELECT * 
        FROM Accounts 
        WHERE Username = ?
        """, (username,))
        return query.fetchone()
    #------------Export function-----------

    def createInsertStatement(self, masteraccountData, upPasswordData):
        self.cur.execute("""
        Insert into Accounts(UserName, MasterPassword)
        VALUES (?, ?)
        """, (masteraccountData[0], masteraccountData[1]))

        self.cur.execute("""
        
        """)
        for site in upPasswordData:
            self.cur.execute("""
            insert into userpasswords (site, siteusername, password, masterusername)
            VALUES (?, ?, ?, ?)
            """, (site[0], site[1], site[2], site[3]))
        self.con.commit()

    #----------Check if User Exists----------
    def user_exists(self, username):
        userexists = """
        Select Exists(
            Select * from accounts
            Where username = ?)
        """
        query = self.cur.execute(userexists, (username,))
        return query.fetchone()[0]

