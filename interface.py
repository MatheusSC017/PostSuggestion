from PyQt6.QtWidgets import QApplication

from ui.window import MainWindow

app = QApplication([])
main = MainWindow()
main.show()
app.exec()
