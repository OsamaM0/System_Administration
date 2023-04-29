from MainApplication.GUI.MainGUI_Commands import MainApplicationRun
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from MainApplication.GUI.MainGUI_Commands  import *
from MainApplication.Database.DatabaseCommands  import DatabaseCommands as dbc
from MainApplication.LogIn.LoginGUI import Ui_Form
from MainApplication.LogIn.Login_commands import Login


def check_login(username, password):
    
    # Check the user name and password
    for user in users:
            if (user["UserName"] == username) and (password==user["Password"]):
                # If the user name and password are correct, close the login UI and show the main window UI
                login_ui.close()
                MainApplicationRun(username)
                break
            
    else:
        # If the user name and password are incorrect, display an error message
        QtWidgets.QMessageBox.warning(login_ui, 'Error', 'Invalid username or password')
        
        
    
if __name__ == "__main__":  

        app = QApplication(sys.argv)
        
        # Connect to Database 
        database = dbc()
        users = database.select(table="User")

        # Create a main window and a button
        login_ui = Login()
        login_ui.login_signal.connect(check_login)
        login_ui.show()

        sys.exit(app.exec_())