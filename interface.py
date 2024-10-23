from PyQt6.QtWidgets import QApplication

from UI.window import MainWindow

app = QApplication([])
main = MainWindow()
main.show()
app.exec()
