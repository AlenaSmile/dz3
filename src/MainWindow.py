from PyQt5.QtWidgets import (
    QMainWindow, QMessageBox
)
from PyQt5.QtCore import pyqtSlot
from MainMenu import MainMenu
from src import Test


class MainWindow(QMainWindow):
    def __init__(self, conn, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Управление заданиями для учащихся')
        main_menu = MainMenu(parent=self)
        self.setMenuBar(main_menu)
        w = Test.View(conn, parent=self)
        self.setCentralWidget(w)
        main_menu.about.triggered.connect(self.about)
        main_menu.about_qt.triggered.connect(self.about_qt)
        #main_menu.teacher_add.triggered.connect(w.add)
        #main_menu.teacher_edit.triggered.connect(w.update)
        #main_menu.teacher_delete.triggered.connect(w.delete)
        main_menu.test_add.triggered.connect(w.add)
        main_menu.test_delete.triggered.connect(w.delete)

    @pyqtSlot()
    def about(self):
        title = 'Управление заданиями для учащихся'
        text = (
            'Программа для управления задачами\n' +
            'и заданиями для учащихся школы'
        )
        QMessageBox.about(self, title, text)

    @pyqtSlot()
    def about_qt(self):
        QMessageBox.aboutQt(self, 'Управление заданиями для учащихся')
