import sys, os
from distutils.log import Log
import sys
import PyQt5
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
import tkinter
from tkinter import filedialog
import pyperclip
import sql
import useraccount as ua



ActiveUser = ua.User()


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
    def clickLogin(self):
        acc = AccountScreen()
        widget.addWidget(acc)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.removeWidget(self)

    def gotoCreateAccount(self):
        ca = CreateAccountScreen()
        widget.addWidget(ca)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.removeWidget(self)

    def getExternalDB(self):
        tkinter.Tk().withdraw()
        dbpath = filedialog.askdirectory()
        db.setPath(dbpath)
        db.initialize_db()
        db.setConnection()
#-------------End Login Screen----------------------------


#-------------Create Account Screen-----------------------
# This is where user will create main account to log into PassMan

class CreateAccountScreen(QDialog):
    def __init__(self) :
        super(CreateAccountScreen, self).__init__()
        loadUi((os.path.join(os.getcwd(), 'createAccountScreen.ui')), self)
        self.errormessageLabel.setVisible(False)
        self.gobackButton.clicked.connect(self.goBack)

    def goBack(self):
        li = LoginScreen()
        widget.addWidget(li)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.removeWidget(self)
#------------End Create Account Screen-------------------------



#-------------Account Screen-------------------------------------
#This is where user will access stored passwords under their main account

class AccountScreen(QDialog):
    def __init__(self) :
        super(AccountScreen, self).__init__()
        loadUi((os.path.join(os.getcwd(), 'AccountScreen.ui')), self)        
        self.logoutButton.clicked.connect(self.logout)
        self.addaccountButton.clicked.connect(self.gotoAddAccount)
        self.exportaccountButton.clicked.connect(self.ExportAccount)
    
    def logout(self):
        li = LoginScreen()
        widget.addWidget(li)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.removeWidget(self)

    def gotoAddAccount(self):
        aa = AddAccountScreen()
        widget.addWidget(aa)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.removeWidget(self)

    def ExportAccount(self):
        export = sql.Database()
        tkinter.Tk().withdraw()
        dbpath = filedialog.askdirectory()
        export.setPath(dbpath)

        
#---------------End Account Screen------------------------


#---------------Add Account Screen---------------------------------
#This is where user will add passwords to their main user account

class AddAccountScreen(QDialog):
    def __init__(self) :
        super(AddAccountScreen, self).__init__()
        loadUi((os.path.join(os.getcwd(), 'AddAccountScreen.ui')), self)
        self.errormessageLabel.setVisible(False)
        value = self.passwordlengthSlider.value()
        self.passwordlengthDisplay.display(value)
        self.gobackButton.clicked.connect(self.goBack)
        self.enablepasswordgencheckBox.stateChanged.connect(self.enablePWGen)        
        self.passwordlengthSlider.valueChanged.connect(self.updatePasswordLengthDisplay)


    def enablePWGen(self):        
        self.passwordlengthSlider.setEnabled(self.enablepasswordgencheckBox.isChecked())
        self.uppercasecheckBox.setEnabled(self.enablepasswordgencheckBox.isChecked()) 
        self.lowercasecheckBox.setEnabled(self.enablepasswordgencheckBox.isChecked()) 
        self.numberscheckBox.setEnabled(self.enablepasswordgencheckBox.isChecked()) 
        self.symbolscheckBox.setEnabled(self.enablepasswordgencheckBox.isChecked())
        self.generatepasswordButton.setEnabled(self.enablepasswordgencheckBox.isChecked())
    

    def updatePasswordLengthDisplay(self):
        value = self.passwordlengthSlider.value()
        self.passwordlengthDisplay.display(value)


    def goBack(self):
        acc = AccountScreen()
        widget.addWidget(acc)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.removeWidget(self)

#---------------End Add Account Screen---------------------------------    
    


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