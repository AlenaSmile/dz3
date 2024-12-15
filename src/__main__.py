import sys
from Application import Application
from MainWindow import MainWindow

app = Application(sys.argv)
main_window = MainWindow(app.db_conn)
main_window.setGeometry(500, 500, 800, 400)
main_window.show()

result = app.exec()
sys.exit(result)