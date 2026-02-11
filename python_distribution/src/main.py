
import sys
import os
import datetime
import logging
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QApplication
from PyQt5.uic import loadUiType
import sqlite3
from xlsxwriter import Workbook
from .database import get_db_connection

logger = logging.getLogger(__name__)

# Ensure resources are importable before loading UI
res_path = os.path.join(os.path.dirname(__file__), 'res')
sys.path.append(res_path)

# Load UI file
ui_path = os.path.join(res_path, 'app_design.ui')
try:
    ui, _ = loadUiType(ui_path)
except Exception as e:
    logger.critical(f"Error loading UI file {ui_path}: {e}")
    sys.exit(1)

try:
    import icons_rc
except ImportError:
    logger.warning("icons_rc not found or failed to import.")
    pass 

class Library(QMainWindow, ui):
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.buttons()
        self.handleUiTab()
        
        # Initialize UI with data
        try:
             self.show_categories()
             self.show_author()
             self.show_publisher()
             self.bookCategoryForEditDeleteTab()
             self.authorForEditDeleteTab()
             self.publisherForEditDeleteTab()
             self.bookCategoryForAddTab()
             self.authorForAddTab()
             self.publisherForAddTab()
             self.show_client()
             self.showAllBooks()
             self.show_day_operations()
        except Exception as e:
            logger.error(f"Initialization error (non-fatal): {e}")

    
    def buttons(self):
        self.dayOperationBtn.clicked.connect(self.day_operationsTab)
        self.booksBtn.clicked.connect(self.booksTab)
        self.userBtn.clicked.connect(self.usersTab)
        self.settingsBtn.clicked.connect(self.settingsTab)
        self.clientBtn.clicked.connect(self.clientTab)
        
        self.addBookBtn.clicked.connect(self.addBook)
        self.bookSearchBtn.clicked.connect(self.searchBook)
        self.updateBookInfo.clicked.connect(self.editBook)
        self.deleteBookBtn.clicked.connect(self.deleteBook)
        
        self.addCategoryBtn.clicked.connect(self.add_categories)
        self.addAuthorBtn.clicked.connect(self.add_author)
        self.addPublisherBtn.clicked.connect(self.add_publisher)
        
        self.addUserBtn.clicked.connect(self.addNewUser)
        self.userLogin.clicked.connect(self.UserLogin)
        self.userUpadteBtn.clicked.connect(self.updateUser)
        
        self.addClientBtn.clicked.connect(self.add_client)
        self.searchClientBtn.clicked.connect(self.search_client)
        self.updateClientBtn.clicked.connect(self.update_client)
        self.deleteClientBtn.clicked.connect(self.delete_client)
        
        self.dayOprBtn.clicked.connect(self.addDayOperations)
        
        self.dayoperationsExcel.clicked.connect(self.export_day_operations)
        self.booksExcel.clicked.connect(self.export_books)
        self.clientExcel.clicked.connect(self.export_clients)
    
    def handleUiTab(self):
        self.tabWidget.tabBar().setVisible(False)
    
    def day_operationsTab(self):
        self.tabWidget.setCurrentIndex(0)
    
    def booksTab(self):
        self.tabWidget.setCurrentIndex(1)
        
    def clientTab(self):
        self.tabWidget.setCurrentIndex(2)
    
    def usersTab(self):
        self.tabWidget.setCurrentIndex(3)
    
    def settingsTab(self):
        self.tabWidget.setCurrentIndex(4)
    
    ############# book operation #############
    def addBook(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            
            bookName = self.bookTitle.text()
            bookcode = self.bookCode.text()
            bookcategory = self.bookCategory.currentText()
            bookauthor = self.bookAuthor.currentText()
            bookpublisher = self.bookPublisher.currentText()
            bookPrice = self.bookPrice.text()
            bookDescription = self.addBookTabDescription.toPlainText()
            
            self.cur.execute('''
                INSERT INTO book(book_name, book_description, book_code, book_category, book_author, book_publisher, book_price) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',(bookName, bookDescription, bookcode, bookcategory, bookauthor, bookpublisher, bookPrice))
            self.db.commit()
            self.statusBar().showMessage('new book is added successfully..')
            
            self.bookTitle.setText('')
            self.bookCode.setText('')
            self.bookCategory.setCurrentIndex(0)
            self.bookAuthor.setCurrentIndex(0)
            self.bookPublisher.setCurrentIndex(0)
            self.bookPrice.setText('')
            self.addBookTabDescription.setPlainText('')
            self.showAllBooks()
            self.db.close()
        except sqlite3.Error as e:
             self.statusBar().showMessage(f'Error adding book: {e}')
    
    def searchBook(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            searchedBookName = self.searchBookName.text()
            sql = "SELECT * FROM book WHERE book_name=?"
            self.cur.execute(sql, [(searchedBookName)])
            data = self.cur.fetchone()
            if data:
                self.searchBookTitle.setText(data[1])
                self.searchBookCode.setText(data[3])
                self.searchBookPrice.setText(str(data[7]))
                self.editDelBookTabDescription.setPlainText(str(data[2]))
            else:
                self.statusBar().showMessage('Book not found')
            self.db.close()
        except sqlite3.Error as e:
            self.statusBar().showMessage(f'Error searching book: {e}')
    
    def editBook(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            
            searchBookTitle = self.searchBookName.text()
            
            bookName = self.searchBookTitle.text()
            bookcode = self.searchBookCode.text()
            bookcategory = self.availableCategory.currentText()
            bookauthor = self.availablAuthor.currentText()
            bookpublisher = self.availablePublisher.currentText()
            bookPrice = self.searchBookPrice.text()
            bookDescription = self.editDelBookTabDescription.toPlainText()
            
            self.cur.execute('''
            UPDATE book SET book_name=?, book_description=?, book_code=?, book_category=?, book_author=?, book_publisher=?, book_price=? WHERE book_name=?
            ''', (bookName,bookDescription,bookcode,bookcategory,bookauthor,bookpublisher,bookPrice,searchBookTitle))
            self.db.commit()
            self.statusBar().showMessage('book is updated..')
            self.showAllBooks()
            self.db.close()
        except sqlite3.Error as e:
            self.statusBar().showMessage(f'Error updating book: {e}')
    
    def deleteBook(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            
            searchBookTitle = self.searchBookName.text()
            permission = QMessageBox.warning(self, 'delete book', 'do you want to delete the book', QMessageBox.Yes|QMessageBox.No)
            if permission == QMessageBox.Yes:
                delQuery = "DELETE FROM book WHERE book_name=?"
                self.cur.execute(delQuery, [(searchBookTitle)])
                self.db.commit()
                self.statusBar().showMessage('book is deleted..')
                self.showAllBooks()
            
            self.searchBookName.setText('')
            self.searchBookTitle.setText('')
            self.searchBookCode.setText('')
            self.availableCategory.setCurrentIndex(0)
            self.availablAuthor.setCurrentIndex(0)
            self.availablePublisher.setCurrentIndex(0)
            self.searchBookPrice.setText('')
            self.editDelBookTabDescription.setPlainText('')
            self.db.close()
        except sqlite3.Error as e:
            self.statusBar().showMessage(f'Error deleting book: {e}')
    
    def showAllBooks(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            
            self.cur.execute("SELECT book_code,book_name,book_author,book_publisher,book_category,book_price FROM book")
            data = self.cur.fetchall()
            if data:
                row_count = 0
                self.tableWidget_3.setRowCount(0) # Clear existing rows
                for row, form in enumerate(data):
                    self.tableWidget_3.insertRow(row_count)
                    for col, item in enumerate(form):
                        self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(item)))
                    row_count += 1
            self.db.close()
        except sqlite3.Error as e:
             logger.error(f"Error fetching books: {e}")
        
    # *********** day operation ************
    # **************************************
    
    def addDayOperations(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            
            bookName = self.dayOprBook.text()
            clientName = self.dayOprClient.text()
            typ = self.dayOprTypSel.currentText()
            day = self.dayOprDaySel.currentIndex() + 1
            fromdate = datetime.date.today()
            todate = fromdate + datetime.timedelta(days=3) # Assuming 3 days return policy?
            
            self.cur.execute("INSERT INTO dayoperations(bookname,type,days,fromDate,toDate,clientName) VALUES(?, ?, ?, ?, ?, ?)",(bookName,typ,day,fromdate,todate,clientName))
            self.db.commit()
            self.statusBar().showMessage('new operation is added..')
            self.show_day_operations()
            self.db.close()
        except sqlite3.Error as e:
            self.statusBar().showMessage(f'Error adding operation: {e}')
    
    def show_day_operations(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            
            self.cur.execute("SELECT bookname,clientName,type,fromDate,toDate FROM dayoperations")
            data = self.cur.fetchall()
            if data:
                row_count = 0
                self.tableWidget_2.setRowCount(0)
                for row, form in enumerate(data):
                    self.tableWidget_2.insertRow(row_count)
                    for col, item in enumerate(form):
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
                    row_count += 1
            self.db.close()
        except sqlite3.Error as e:
             logger.error(f"Error showing day operations: {e}")
            
        
     ############# user operation #############
    def addNewUser(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            
            username = self.regUsername.text()
            mail = self.regEmail.text()
            password = self.regPass.text()
            rePassword = self.regPassAgain.text()
            
            if password == rePassword:
                self.cur.execute("INSERT INTO users(username, useremail, userspassword) VALUES(?, ?, ?)", (username, mail, password))
                self.db.commit()
                self.statusBar().showMessage('new user is added successfully.....')
                self.errorMsg.setText('')
            else:
                self.errorMsg.setText('password is not matched....')
                self.statusBar().showMessage(' ')
            self.db.close()
        except sqlite3.Error as e:
            self.statusBar().showMessage(f'Error adding user: {e}')
    
    def UserLogin(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            
            loginUsername = self.userloginUsername.text()
            loginUserPass = self.userloginPass.text()
            
            sql = "SELECT * FROM users"
            self.cur.execute(sql)
            data = self.cur.fetchall()
            found = False
            for d in data:
                if d[1] == loginUsername and d[3] == loginUserPass:
                    self.edituserInfo.setEnabled(True)
                    self.statusBar().showMessage('login successful...')
                    
                    self.editUserUsername.setText(d[1])
                    self.editUserMail.setText(d[2])
                    self.editUserPass.setText(d[3])
                    found = True
                    break
            if not found:
                self.statusBar().showMessage('username or password is invalid...')
            self.db.close()
        except sqlite3.Error as e:
             self.statusBar().showMessage(f'Error logging in: {e}')
    
    def updateUser(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            
            updateUsername = self.editUserUsername.text()
            updateUserMail = self.editUserMail.text()
            updateUserPass = self.editUserPass.text()
            updateUserPassAgain = self.lineEdit_17.text()
            beforeUpdateUsername = self.userloginUsername.text()
            
            if updateUserPass == updateUserPassAgain:
                self.cur.execute('''
                UPDATE users SET username=?, useremail=?, userspassword=? WHERE username=?
                ''',(updateUsername, updateUserMail, updateUserPass, beforeUpdateUsername))
                self.db.commit()
                self.statusBar().showMessage('user information is updated')
            else:
                self.statusBar().showMessage('password is not matched')
            self.db.close()
        except sqlite3.Error as e:
            self.statusBar().showMessage(f'Error updating user: {e}')
    
    ############# client operation #############
    
    def add_client(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            
            clientName = self.newClientName.text()
            clientEmail = self.newClientEmail.text()
            clientId = self.newClientId.text()
            
            self.cur.execute("INSERT INTO client(clientName, clientEmail, clientNid) VALUES(?, ?, ?)", (clientName, clientEmail, clientId))
            self.db.commit()
            self.statusBar().showMessage('new client is added')
            self.show_client()
            self.db.close()
        except sqlite3.Error as e:
            self.statusBar().showMessage(f"Error adding client: {e}")

    def search_client(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            
            searchclient = self.searchClient.text()
            sql = "SELECT * FROM client WHERE clientNid=?"
            self.cur.execute(sql, [(searchclient)])
            data = self.cur.fetchone()
            if data:
                self.updelClientName.setText(data[1])
                self.updelClientEmail.setText(data[2])
                self.updelClientId.setText(data[3])
            else:
                 self.statusBar().showMessage('Client not found')
            self.db.close()
        except sqlite3.Error as e:
            self.statusBar().showMessage(f"Error searching client: {e}")
        
    def update_client(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            
            upclientName = self.updelClientName.text()
            upclientEmail = self.updelClientEmail.text()
            upclientId = self.updelClientId.text()
            searchedclientId = self.searchClient.text()
            if upclientName and upclientEmail and upclientId:
                 self.cur.execute("UPDATE client SET clientName=?, clientEmail=?, clientNid=? WHERE clientNid=?", (upclientName,upclientEmail,upclientId,searchedclientId))
                 self.db.commit()
                 self.statusBar().showMessage('client information is updated...')
                 self.show_client()
            else:
                self.clientUperror.setText('fields are required....')
            self.db.close()
        except sqlite3.Error as e:
            self.statusBar().showMessage(f"Error updating client: {e}")
            
    def show_client(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            self.cur.execute("SELECT * FROM client")
            data = self.cur.fetchall()
            if data:
                row_count = 0
                self.tableWidget.setRowCount(0)
                for row, form in enumerate(data):
                    self.tableWidget.insertRow(row_count)
                    for col, item in enumerate(form):
                        self.tableWidget.setItem(row, col, QTableWidgetItem(str(item)))
                    row_count += 1
            self.db.close()
        except sqlite3.Error as e:
             logger.error(f"Error showing clients: {e}")
        
    def delete_client(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()

            searchedclientId = self.searchClient.text()
            if searchedclientId:
                permission = QMessageBox.warning(self,'delete client', 'are you sure to delete the client', QMessageBox.Yes|QMessageBox.No)
                if permission == QMessageBox.Yes:
                    sql = "DELETE FROM client WHERE clientNid=?"
                    self.cur.execute(sql, [(searchedclientId)])
                    self.db.commit()
                    self.statusBar().showMessage('information is deleted successfully...')
                    self.show_client()
            else:
                self.clientUperror.setText('client id field is required...')
            self.db.close()
        except sqlite3.Error as e:
            self.statusBar().showMessage(f"Error deleting client: {e}")
        
    
    ############# setting operation #############
    
    def add_author(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            
            authorname = self.addAuthor.text()
            self.cur.execute("INSERT INTO author(author_name) VALUES (?)", (authorname,))
            self.db.commit()
            self.statusBar().showMessage('new author is added successfully...')
            self.show_author()
            self.authorForEditDeleteTab()
            self.authorForAddTab()
            print('author is added successfully...')
            self.db.close()
        except sqlite3.Error as e:
            self.statusBar().showMessage(f"Error adding author: {e}")
    
    def show_author(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            self.cur.execute("SELECT author_name FROM author") 
            data = self.cur.fetchall()
            if data:
                row_count = 0
                self.allAuthors_2.setRowCount(0)
                for row, form in enumerate(data):
                    self.allAuthors_2.insertRow(row_count)
                    for col, item in enumerate(form):
                        self.allAuthors_2.setItem(row, col, QTableWidgetItem(str(item)))
                    row_count += 1
            self.db.close()
        except sqlite3.Error as e:
             logger.error(f"Error showing authors: {e}")
    
    def add_categories(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            
            categoryname = self.categoryName.text()
            self.cur.execute("INSERT INTO category(category_name) VALUES (?)", (categoryname,))
            self.db.commit()
            self.statusBar().showMessage('new book category is added successfully...')
            self.show_categories()
            self.bookCategoryForEditDeleteTab()
            self.bookCategoryForAddTab()
            print('book category is added successfully...')
            self.db.close()
        except sqlite3.Error as e:
            self.statusBar().showMessage(f"Error adding category: {e}")
        
    def show_categories(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            self.cur.execute("SELECT category_name FROM category") 
            data = self.cur.fetchall()
            if data:
                row_count = 0
                self.allCategories.setRowCount(0)
                for row, form in enumerate(data):
                    self.allCategories.insertRow(row_count)
                    for col, item in enumerate(form):
                        self.allCategories.setItem(row, col, QTableWidgetItem(str(item)))
                    row_count += 1
            self.db.close()
        except sqlite3.Error as e:
             logger.error(f"Error showing categories: {e}")
                
    
    def add_publisher(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            
            publishername = self.addPublisher.text()
            self.cur.execute("INSERT INTO publisher(publisher_name) VALUES (?)", (publishername,))
            self.db.commit()
            self.statusBar().showMessage('new publisher is added successfully...')
            self.show_publisher()
            self.publisherForEditDeleteTab()
            self.publisherForAddTab()
            print('publisher is added successfully...')
            self.db.close()
        except sqlite3.Error as e:
            self.statusBar().showMessage(f"Error adding publisher: {e}")
    
    def show_publisher(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            self.cur.execute("SELECT publisher_name FROM publisher") 
            data = self.cur.fetchall()
            if data:
                row_count = 0
                self.allPublishers.setRowCount(0)
                for row, form in enumerate(data):
                    self.allPublishers.insertRow(row_count)
                    for col, item in enumerate(form):
                        self.allPublishers.setItem(row, col, QTableWidgetItem(str(item)))
                    row_count += 1
            self.db.close()
        except sqlite3.Error as e:
             logger.error(f"Error showing publishers: {e}")
    
    def bookCategoryForAddTab(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            self.cur.execute("SELECT category_name FROM category")
            data = self.cur.fetchall()
            for d in data:
                self.bookCategory.addItem(d[0])
            self.db.close()
        except sqlite3.Error as e:
             logger.error(f"Error fetching categories: {e}")
    
    def authorForAddTab(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            self.cur.execute("SELECT author_name FROM author")
            data = self.cur.fetchall()
            for d in data:
                self.bookAuthor.addItem(d[0])
            self.db.close()
        except sqlite3.Error as e:
             logger.error(f"Error fetching authors: {e}")
    
    def publisherForAddTab(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            self.cur.execute("SELECT publisher_name FROM publisher")
            data = self.cur.fetchall()
            for d in data:
                self.bookPublisher.addItem(d[0])
            self.db.close()
        except sqlite3.Error as e:
             logger.error(f"Error fetching publishers: {e}")
    
    def bookCategoryForEditDeleteTab(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            self.cur.execute("SELECT category_name FROM category")
            data = self.cur.fetchall()
            for d in data:
                self.availableCategory.addItem(d[0])
            self.db.close()
        except sqlite3.Error as e:
             logger.error(f"Error fetching categories: {e}")
    
    def authorForEditDeleteTab(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            self.cur.execute("SELECT author_name FROM author")
            data = self.cur.fetchall()
            for d in data:
                self.availablAuthor.addItem(d[0])
            self.db.close()
        except sqlite3.Error as e:
             logger.error(f"Error fetching authors: {e}")
    
    def publisherForEditDeleteTab(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            self.cur.execute("SELECT publisher_name FROM publisher")
            data = self.cur.fetchall()
            for d in data:
                self.availablePublisher.addItem(d[0])
            self.db.close()
        except sqlite3.Error as e:
             logger.error(f"Error fetching publishers: {e}")
    
    # *********** Export ***********
    # *****************************
    def export_day_operations(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            
            self.cur.execute("SELECT bookname,clientName,type,fromDate,toDate FROM dayoperations")
            data = self.cur.fetchall()
            wb = Workbook('day_operations.xlsx')
            sheet1 = wb.add_worksheet()
            sheet1.write(0,0, 'bookname')
            sheet1.write(0,1, 'clientName')
            sheet1.write(0,2, 'type')
            sheet1.write(0,3, 'fromDate')
            sheet1.write(0,4, 'toDate')
            row_num = 1
            for row in data:
                col_num = 0
                for item in row:
                    sheet1.write(row_num, col_num,str(item))
                    col_num +=1
                row_num += 1
            wb.close()
            self.statusBar().showMessage('data is downloaded successfully....')
            self.db.close()
        except sqlite3.Error as e:
            self.statusBar().showMessage(f"Error exporting day operations: {e}")

    def export_books(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            
            self.cur.execute("SELECT book_code,book_name,book_author,book_publisher,book_category,book_price FROM book")
            data = self.cur.fetchall()
            wb = Workbook('allBooks.xlsx')
            sheet1 = wb.add_worksheet()
            sheet1.write(0,0, 'book_code')
            sheet1.write(0,1, 'book_name')
            sheet1.write(0,2, 'book_author')
            sheet1.write(0,3, 'book_publisher')
            sheet1.write(0,4, 'book_category')
            sheet1.write(0,5, 'book_price')
            row_num = 1
            for row in data:
                col_num = 0
                for item in row:
                    sheet1.write(row_num, col_num,str(item))
                    col_num +=1
                row_num += 1
            wb.close()
            self.statusBar().showMessage('data is downloaded successfully....')
            self.db.close()
        except sqlite3.Error as e:
            self.statusBar().showMessage(f"Error exporting books: {e}")

    def export_clients(self):
        try:
            self.db = get_db_connection(self)
            if not self.db: return
            self.cur = self.db.cursor()
            self.cur.execute("SELECT clientName,clientEmail,clientNid FROM client")
            data = self.cur.fetchall()
            wb = Workbook('allClients.xlsx')
            sheet1 = wb.add_worksheet()
            sheet1.write(0,0, 'clientName')
            sheet1.write(0,1, 'clientEmail')
            sheet1.write(0,2, 'clientNid')
            row_num = 1
            for row in data:
                col_num = 0
                for item in row:
                    sheet1.write(row_num, col_num,str(item))
                    col_num +=1
                row_num += 1
            wb.close()
            self.statusBar().showMessage('data is downloaded successfully....')
            self.db.close()
        except sqlite3.Error as e:
            self.statusBar().showMessage(f"Error exporting clients: {e}")

if __name__ == '__main__':
    # For testing this file directly, though run.py is preferred
    app = QApplication(sys.argv)
    win = Library() # Note: This usually requires login first
    win.show()
    app.exec_()
