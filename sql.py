import sqlite3 
import os

class Database:
    def __init__(self) -> None:
        self.dbpath = os.path.dirname(os.path.realpath(__file__))
    
    
    def getPath(self):
        return self.dbpath

    def initialize_db(self, dbpath):
        con = sqlite3.connect(os.path.join(dbpath, 'passMan.db') )
        cur = con.cursor()
        cur.execute("""
        create table if not exists accounts(   
            UserName varchar(255) Primary Key ,
            MasterPassword varchar(255))
        """)

        cur.execute("""
        create table if not exists userpasswords(   
            AccountEntry integer Primary Key,
            Site varchar(255),
            SiteUserName varchar(255),
            Password varchar(255),
            MasterUserName varchar(255),
            Foreign Key (MasterUserName) References accounts(UserName)
            )
        """)
        con.commit()