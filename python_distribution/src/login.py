
import sys
import os
import logging
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QMessageBox
from PyQt5.uic import loadUiType
import sqlite3
from .database import get_db_connection

logger = logging.getLogger(__name__)

# Load UI file
ui_path = os.path.join(os.path.dirname(__file__), 'res', 'login.ui')
logger.debug(f"Loading Login UI from: {ui_path}")
try:
    loginUi, _ = loadUiType(ui_path)
    logger.debug("Login UI loaded successfully.")
except Exception as e:
    logger.critical(f"Error loading UI file {ui_path}: {e}")
    sys.exit(1)

class LoginCls(QMainWindow, loginUi):
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        logger.debug("Login window setup complete.")
        self.loginBtn.clicked.connect(self.handleLogin)
        self.password_field = self.findChild(QLineEdit, 'loginUserPass') 
        if self.password_field:
            self.password_field.setEchoMode(QLineEdit.Password)

        self.mainWindow = None # Will be set to Library instance

    def handleLogin(self):
        try:
            self.db = get_db_connection(self)
            if not self.db:
                return # User cancelled or failed
                
            self.cur = self.db.cursor()
            
            loginUsername = self.loginUsername.text()
            loginUserPass = self.loginUserPass.text()
            
            sql = "SELECT * FROM users"
            self.cur.execute(sql)
            data = self.cur.fetchall()
            found = False
            for d in data:
                # d[1] is username, d[3] is password
                if d[1] == loginUsername and d[3] == loginUserPass:
                    from .main import Library # Cyclic import if at top level
                    self.mainWindow = Library()
                    self.close()
                    self.mainWindow.show()
                    found = True
                    break
            if not found:
                self.loginError.setText('Username or password is invalid...')
            self.db.close()
            
        except sqlite3.Error as e:
            self.loginError.setText(f"Database Error: {e}")
        except Exception as e:
            self.loginError.setText(f"Error: {e}")
            import traceback
            traceback.print_exc()
