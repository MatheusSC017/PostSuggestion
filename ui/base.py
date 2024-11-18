from PyQt6.QtWidgets import QMessageBox


class ErrorHandling:
    def error_handling(self, message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Error")
        dlg.setText(message)
        dlg.exec()
