import sys, os
from distutils.log import Log
import sys
import PyQt5
from PyQt5 import QtGui
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QListWidget, QMenu, QAction, QLineEdit
from PyQt5.QtCore import QEvent, Qt
import tkinter
from tkinter import filedialog
import pyperclip
import sql
import useraccount as ua
import encryption as enc


ActiveUser = ua.User()

width, height = 300,700
def NewScreen (currentscreen, newscreen):
    widget.addWidget(newscreen)
    widget.setCurrentIndex(widget.currentIndex() + 1)
    widget.removeWidget(currentscreen)
#---------------------Login Screen---------------------------------------
#Starting screen This is where users will log into their main account



class LoginScreen(QDialog):
    def __init__(self) :
        super(LoginScreen, self).__init__()
        loadUi((os.path.join(os.getcwd(), 'LoginScreen.ui')), self)        
        self.errormessageLabel.setVisible(False)
        self.loginButton.clicked.connect(self.clickLogin)
        self.createaccountButton.clicked.connect(self.gotoCreateAccount)
        self.useexternalaccountButton.clicked.connect(self.getExternalDB)
        self.deleteaccountButton.clicked.connect(self.gotoDeleteAccount)
        
        self.setContentsMargins


    def clickLogin(self):
        username = self.usernameInput.text()
        pw = self.passwordInput.text()
        
        if username:
            if db.user_exists(username):
                dbpw = db.selectPassword(username)
                if enc.check_password(pw, dbpw):
                    ActiveUser.login(username, pw, dbpw) 
                        
                    acc = AccountScreen()
                    widget.addWidget(acc)
                    widget.setCurrentIndex(widget.currentIndex() + 1)
                    widget.removeWidget(self)
                else:
                    self.errormessageLabel.setText("Password is incorrect")
                    self.errormessageLabel.setVisible(True)
            else:
                self.errormessageLabel.setText("Username does not exist")
                self.errormessageLabel.setVisible(True)

    def gotoCreateAccount(self):
        ca = CreateAccountScreen()
        NewScreen(self, ca)

    def getExternalDB(self):
        tkinter.Tk().withdraw()
        dbpath = filedialog.askopenfilename(title = 'Please select your external account location', filetypes=[('Database Files', ['.db'])])
        if dbpath:
            filepath = os.path.abspath(dbpath)            
            db.setPath(filepath)
            db.initialize_db()
            db.setConnection()

    def gotoDeleteAccount(self):
        da = DeleteAccountScreen()
        NewScreen(self, da)

#-------------End Login Screen----------------------------

#-------------Create Account Screen-----------------------
# This is where user will create main account to log into PassMan

class CreateAccountScreen(QDialog):
    def __init__(self) :
        super(CreateAccountScreen, self).__init__()
        loadUi((os.path.join(os.getcwd(), 'createAccountScreen.ui')), self)
        self.errormessageLabel.setVisible(False)
        self.gobackButton.clicked.connect(self.goBack)
        self.createaccountButton.clicked.connect(self.createAccount)        
        self.setMinimumSize(width, height-400)

    def goBack(self):
        li = LoginScreen()
        NewScreen(self, li)

    def createAccount(self):
        username = self.usernameInput.text()
        pw = self.passwordInput.text()
        cpw = self.confirmpasswordInput.text()
        if db.user_exists(username):
            self.errormessageLabel.setText("User account already exists for that username")
            self.errormessageLabel.setVisible(True)
        elif pw!=cpw:
            self.errormessageLabel.setText("Passwords do not Match")
            self.errormessageLabel.setVisible(True)
        else:
            hpw = enc.get_hashed_password_and_salt(pw)
            db.insertNewUser(username, hpw)
            self.goBack()
#------------End Create Account Screen-------------------------



#-------------Account Screen-------------------------------------
#This is where user will access stored passwords under their main account

class AccountScreen(QDialog):
    def __init__(self) :
        super(AccountScreen, self).__init__()
        loadUi((os.path.join(os.getcwd(), 'AccountScreen.ui')), self)
        self.welcomeLabel.setText(f"{ActiveUser.getUser()}")        
        self.logoutButton.clicked.connect(self.logout)
        self.addaccountButton.clicked.connect(self.gotoAddAccount)
        self.exportaccountButton.clicked.connect(self.ExportAccount)     
        self.updatemasterpasswordButton.clicked.connect(self.gotoUpdatePassword)
        self.userpasswords = db.selectuserPasswordsData(ActiveUser.getUser())
        self.setMinimumSize(width, height)


        for i,up in enumerate(self.userpasswords):
            item = QtWidgets.QListWidgetItem()
            item.setData(QtCore.Qt.UserRole, i)
            item.setText(f'Site: {up[1]}\nUsername: {up[2]}')
            item.setTextAlignment(Qt.AlignHCenter)
            self.useraccountsList.addItem(item)
            
            
        
        self.useraccountsList.itemClicked.connect(self.copyPassword)
        self.searchBar.textChanged.connect(self.Search)

        self.useraccountsList.installEventFilter(self)
        
    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.useraccountsList and source.itemAt(event.pos()) is not None:
            rcmenu = QtWidgets.QMenu()
            rcmenu.addAction('Copy Password', self.copyPassword)
            rcmenu.addAction('Change Password', self.changePassword)
            rcmenu.addAction('Delete Password', self.deletePassword)

            if rcmenu.exec_(event.globalPos()):
                try:
                    item = source.itemAt(event.pos())
                    data = item.data(QtCore.Qt.UserRole)
                except:
                    pass
            return True

        return super().eventFilter(source, event)
    
    def logout(self):
        ActiveUser.logout()
        li = LoginScreen()
        db.setPath((os.path.join(os.getenv('LOCALAPPDATA'),'PassMan', 'passman.db')))
        db.setConnection()
        NewScreen(self, li)

    def gotoAddAccount(self):
        aa = AddAccountScreen()
        NewScreen(self, aa)

    def gotoUpdatePassword(self):
        up = UpdatePasswordScreen()
        NewScreen(self, up)

    def ExportAccount(self):
        masteraccount = db.getMasterAccount(ActiveUser.getUser())
        userpasswords = db.selectuserPasswordsData(ActiveUser.getUser())
        export = sql.Database()
        tkinter.Tk().withdraw()
        dbpath = filedialog.asksaveasfilename(defaultextension=".db")
        if dbpath:
            filepath = os.path.abspath(dbpath)
            export.setPath(filepath)
            export.initialize_db()
            export.setConnection()
            export.createInsertStatement(masteraccount, userpasswords)
    
    def Search(self):
        searchterm = self.searchBar.text()
        for i in range(self.useraccountsList.count()):
            if searchterm in self.useraccountsList.item(i).text():
                self.useraccountsList.item(i).setHidden(False)
            else:
                self.useraccountsList.item(i).setHidden(True)

    def copyPassword(self):
        idx = self.useraccountsList.currentRow()
        epw= self.userpasswords[idx][3]
        pyperclip.copy(enc.decrypt_userpassword_password(epw, ActiveUser.decryptkey))

    def changePassword(self):
        idx = self.useraccountsList.currentRow()
        dbidx = self.userpasswords[idx][0]
        aa = AddAccountScreen(dbidx)
        NewScreen(self, aa)

    def deletePassword(self):
        idx = self.useraccountsList.currentRow()
        dbidx = self.userpasswords[idx][0]
        db.deleteUserPasswordsSite(dbidx)
        refresh = AccountScreen()
        NewScreen(self, refresh)
        
        
#---------------End Account Screen------------------------


#---------------Add Account Screen---------------------------------
#This is where user will add passwords to their main user account

class AddAccountScreen(QDialog):
    def __init__(self, idx=None) :
        super(AddAccountScreen, self).__init__()
        loadUi((os.path.join(os.getcwd(), 'AddAccountScreen.ui')), self)
        self.idx = idx
        self.errormessageLabel.setVisible(False)
        value = self.passwordlengthSlider.value()
        self.passwordlengthLabel.setText(f"Password Length: {value}")
        self.gobackButton.clicked.connect(self.goBack)
        self.enablepasswordgencheckBox.stateChanged.connect(self.enablePWGen)
        self.showpasswordcheckBox.stateChanged.connect(self.showPW)        
        self.passwordlengthSlider.valueChanged.connect(self.updatePasswordLengthDisplay)
        
        self.generatepasswordButton.clicked.connect(self.generatePassword)
        self.setMinimumSize(width, height)
        if self.idx is not None:
            data = db.selectsiteInfo(self.idx)
            self.screenLabel.setText('Update Site Password')
            self.sitenameInput.setText(data[1])
            self.usernameInput.setText(data[2])
            self.sitenameInput.setReadOnly(True)
            self.usernameInput.setReadOnly(True)
            self.addaccountButton.setText('Update Account')
            self.addaccountButton.clicked.connect(self.UpdateAccount)
        else:
            self.addaccountButton.clicked.connect(self.AddAccount)

    def generatePassword(self):
        containsUppers = self.uppercasecheckBox.isChecked()
        containsLower = self.lowercasecheckBox.isChecked()
        containsNumbers = self.numberscheckBox.isChecked()
        containsSymbols = self.symbolscheckBox.isChecked()
        contains = [containsUppers, containsLower, containsNumbers, containsSymbols]
        pwlen = self.passwordlengthSlider.value()
        pw = enc.generatePassword(contains, pwlen)
        self.passwordInput.setText(pw)
        self.confirmpasswordInput.setText(pw)

    def showPW(self):
        if self.showpasswordcheckBox.isChecked():
            self.passwordInput.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.passwordInput.setEchoMode(QLineEdit.EchoMode.Password)

    def enablePWGen(self):        
        self.passwordlengthSlider.setEnabled(self.enablepasswordgencheckBox.isChecked())
        self.uppercasecheckBox.setEnabled(self.enablepasswordgencheckBox.isChecked()) 
        self.lowercasecheckBox.setEnabled(self.enablepasswordgencheckBox.isChecked()) 
        self.numberscheckBox.setEnabled(self.enablepasswordgencheckBox.isChecked()) 
        self.symbolscheckBox.setEnabled(self.enablepasswordgencheckBox.isChecked())
        self.generatepasswordButton.setEnabled(self.enablepasswordgencheckBox.isChecked())
    
    def AddAccount(self):
        site = self.sitenameInput.text()
        username = self.usernameInput.text()
        pw = self.passwordInput.text()
        cpw = self.confirmpasswordInput.text()
        if pw != cpw:
            self.errormessageLabel.setText("Passwords do not match")
            self.errormessageLabel.setVisible(True)
        else:
            epw = enc.encrypt_userpasswords_password(pw, ActiveUser.decryptkey)
            db.insertIntoUserPasswords(ActiveUser.getUser(), site, username, epw)
            self.goBack()

    def UpdateAccount(self):
        pw = self.passwordInput.text()
        cpw = self.confirmpasswordInput.text()
        if pw != cpw:
            self.errormessageLabel.setText("Passwords do not match")
            self.errormessageLabel.setVisible(True)
        else:
            epw = enc.encrypt_userpasswords_password(pw, ActiveUser.decryptkey)
            db.updateSiteInfo(self.idx, epw)
            acc = AccountScreen()
            NewScreen(self, acc)
            

    def updatePasswordLengthDisplay(self):
        value = self.passwordlengthSlider.value()
        self.passwordlengthLabel.setText(f"Password Length: {value}")


    def goBack(self):
        acc = AccountScreen()
        NewScreen(self, acc)

    

#---------------End Add Account Screen---------------------------------    


#----------------Delete Account Screen-----------------------------------
class DeleteAccountScreen(QDialog):
    def __init__(self) :
        super(DeleteAccountScreen, self).__init__()
        loadUi((os.path.join(os.getcwd(), 'deleteaccountScreen.ui')), self)   
        self.deleteaccountButton.clicked.connect(self.deleteAccount)
        self.gobackButton.clicked.connect(self.goBack)
        self.errormessageLabel.setVisible(False)

    def deleteAccount(self):
        username = self.usernameInput.text()
        pw = self.passwordInput.text()
        cpw = self.confirmpasswordInput.text()
        dbpw = db.selectPassword(username)
        
        if username and pw and cpw:
            if db.user_exists(username):
                if pw == cpw:
                    if enc.check_password(pw, dbpw):
                        db.deleteUserAccount(username)
                        login = LoginScreen()
                        NewScreen(self, login)
                    else:
                        self.errormessageLabel.setText("Incorrect Password")
                        self.errormessageLabel.setVisible(True)
                else:
                    self.errormessageLabel.setText("Passwords do not Match")
                    self.errormessageLabel.setVisible(True)
            else:
                self.errormessageLabel.setText("User does not exist")
                self.errormessageLabel.setVisible(True)

    def goBack(self):
        li = LoginScreen()
        NewScreen(self, li)

#------------------End Delete Account Screen-------------------------

#-------------------Update Password Screen --------------------------
class UpdatePasswordScreen(QDialog):
    def __init__(self) :
        super(UpdatePasswordScreen, self).__init__()
        loadUi((os.path.join(os.getcwd(), 'UpdatePasswordScreen.ui')), self)   
        self.gobackButton.clicked.connect(self.goBack)
        self.errormessageLabel.setVisible(False)
        self.updatepasswordButton.clicked.connect(self.updateMasterPassword)

    def goBack(self):
        acc = AccountScreen()
        NewScreen(self, acc)

    def updateMasterPassword(self):
        cpw= self.currentpasswordInput.text()
        npw= self.newpasswordInput.text()
        cnpw= self.confirmnewpasswordInput.text()

        if cpw and npw and cnpw: 
            if not enc.check_password(cpw, db.selectPassword(ActiveUser.username)):
                self.errormessageLabel.setText('Current Password is Incorrect')
                self.errormessageLabel.setVisible(True)
            elif npw != cnpw:
                self.errormessageLabel.setText('Passwords do not match')
                self.errormessageLabel.setVisible(True)
            else:
                db.updateMasterPW(ActiveUser.decryptkey, npw, ActiveUser.username, db)
                ActiveUser.login(ActiveUser.username, npw, db.selectPassword(ActiveUser.username))
                acc = AccountScreen()
                NewScreen(self, acc)

        else:
            self.errormessageLabel.setText('All Input Fields must be completed')
            self.errormessageLabel.setVisible(True)

#-------------------End Update Password Screen --------------------------

if __name__=='__main__':
    db = sql.Database()
    db.initialize_db()
    db.setConnection()
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    loginscreen = LoginScreen()
    widget.addWidget(loginscreen)
    widget.show()


    sys.exit(app.exec_())