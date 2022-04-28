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