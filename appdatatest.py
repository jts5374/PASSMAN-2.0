import os

ad = os.getenv('LOCALAPPDATA')
db = os.path.join(ad, 'PassMan', 'passMan.db')
print(db)