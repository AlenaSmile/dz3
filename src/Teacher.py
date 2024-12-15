import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtCore import Qt, pyqtSlot

class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.__db = QSqlDatabase.addDatabase('QPSQL')
        self.__db.setHostName('localhost')
        self.__db.setPort(5432)
        self.__db.setDatabaseName('tester')
        self.__db.setUserName('pguser')
        self.__db.setPassword('12345678')
        if not self.__db.open():
            print('Connection FAILED', file=sys.stderr)

    @property
    def db_conn(self):
        return self.__db

class TeacherModel(QSqlTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTable('teachers')
        self.select()

class TeacherView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = TeacherModel(self)
        self.setModel(self.model)
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)

    @pyqtSlot()
    def add_teacher(self):
        dialog = TeacherDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.model.insertRow(self.model.rowCount())
            self.model.setData(self.model.index(self.model.rowCount()-1, 1), dialog.fio)
            self.model.setData(self.model.index(self.model.rowCount()-1, 2), dialog.phone)
            self.model.setData(self.model.index(self.model.rowCount()-1, 3), dialog.email)
            self.model.setData(self.model.index(self.model.rowCount()-1, 4), dialog.comnt)
            self.model.submitAll()

    @pyqtSlot()
    def update_teacher(self):
        index = self.currentIndex()
        if not index.isValid():
            return
        dialog = TeacherDialog(self)
        dialog.fio = self.model.data(self.model.index(index.row(), 1))
        dialog.phone = self.model.data(self.model.index(index.row(), 2))
        dialog.email = self.model.data(self.model.index(index.row(), 3))
        dialog.comnt = self.model.data(self.model.index(index.row(), 4))
        if dialog.exec_() == QDialog.Accepted:
            self.model.setData(self.model.index(index.row(), 1), dialog.fio)
            self.model.setData(self.model.index(index.row(), 2), dialog.phone)
            self.model.setData(self.model.index(index.row(), 3), dialog.email)
            self.model.setData(self.model.index(index.row(), 4), dialog.comnt)
            self.model.submitAll()

    @pyqtSlot()
    def delete_teacher(self):
        index = self.currentIndex()
        if index.isValid():
            self.model.removeRow(index.row())
            self.model.submitAll()

class TeacherDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Учитель')
        self.fio = ''
        self.phone = ''
        self.email = ''
        self.comnt = ''

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.fio_edit = QLineEdit(self)
        self.phone_edit = QLineEdit(self)
        self.email_edit = QLineEdit(self)
        self.comnt_edit = QLineEdit(self)

        layout.addWidget(QLabel('ФИО:', self))
        layout.addWidget(self.fio_edit)
        layout.addWidget(QLabel('Телефон:', self))
        layout.addWidget(self.phone_edit)
        layout.addWidget(QLabel('E-mail:', self))
        layout.addWidget(self.email_edit)
        layout.addWidget(QLabel('Примечание:', self))
        layout.addWidget(self.comnt_edit)

        buttons = QHBoxLayout()
        ok_btn = QPushButton('OK', self)
        cancel_btn = QPushButton('Отмена', self)
        buttons.addWidget(ok_btn)
        buttons.addWidget(cancel_btn)

        layout.addLayout(buttons)

        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

    @pyqtSlot()
    def accept(self):
        self.fio = self.fio_edit.text()
        self.phone = self.phone_edit.text()
        self.email = self.email_edit.text()
        self.comnt = self.comnt_edit.text()
        super().accept()

if __name__ == '__main__':
    app = Application(sys.argv)
    main_window = QMainWindow()
    teacher_view = TeacherView(main_window)
    main_window.setCentralWidget(teacher_view)
    main_window.setGeometry(500, 500, 800, 400)
    main_window.show()
    sys.exit(app.exec_())