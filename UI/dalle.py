import sys
from math import trunc

from PyQt6.QtCore import QPoint, QRect, Qt
from PyQt6.QtGui import QImage, QPainter, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class DalleMask(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Masking App")
        self.setGeometry(100, 100, 800, 600)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll_image = QScrollArea()
        scroll_image.setWidget(self.image_label)
        scroll_image.setWidgetResizable(True)

        self.load_button = QPushButton("Load Image", self)
        self.load_button.clicked.connect(self.load_image)

        self.clear_button = QPushButton("Clear Mask", self)
        self.clear_button.clicked.connect(self.clear_mask)

        self.export_button = QPushButton("Export Mask as PNG", self)
        self.export_button.clicked.connect(self.export_image)

        layout = QVBoxLayout()
        layout.addWidget(self.load_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.export_button)
        layout.addWidget(scroll_image)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.image = None
        self.mask = None
        self.selection_start = None
        self.selection_end = None

    def load_image(self):
        options = QFileDialog.Option(0)
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Image File", "", "Images (*.png *.xpm *.jpg)", options=options
        )
        if file_name:
            self.image = QImage(file_name)
            self.mask = QImage(self.image.size(), QImage.Format.Format_ARGB32)
            self.mask.fill(Qt.GlobalColor.transparent)
            self.image_label.setPixmap(QPixmap.fromImage(self.image))

            self.image_label.setMouseTracking(True)
            self.image_label.setScaledContents(False)
            self.image_label.mousePressEvent = self.start_selection
            self.image_label.mouseMoveEvent = self.update_selection
            self.image_label.mouseReleaseEvent = self.finish_selection

    def start_selection(self, event):
        self.selection_start = QPoint(
            trunc(event.position().x()), trunc(event.position().y())
        )
        self.selection_end = self.selection_start

    def update_selection(self, event):
        if self.selection_start:
            self.selection_end = QPoint(
                trunc(event.position().x()), trunc(event.position().y())
            )
            self.update_mask()

    def finish_selection(self, event):
        self.selection_end = QPoint(
            trunc(event.position().x()), trunc(event.position().y())
        )
        self.update_mask()
        self.selection_start = None

    def update_mask(self):
        if self.image and self.selection_start and self.selection_end:
            painter = QPainter(self.mask)
            painter.setBrush(Qt.GlobalColor.white)
            painter.setPen(Qt.GlobalColor.white)

            rect = QRect(self.selection_start, self.selection_end).normalized()
            painter.drawRect(rect)
            painter.end()

            combined_image = QImage(self.image.size(), QImage.Format.Format_ARGB32)
            combined_image.fill(Qt.GlobalColor.transparent)
            painter = QPainter(combined_image)
            painter.drawImage(0, 0, self.image)
            painter.drawImage(0, 0, self.mask)
            painter.end()

            self.image_label.setPixmap(QPixmap.fromImage(combined_image))

    def export_image(self):
        if self.image and self.mask:
            combined_image = QImage(self.image.size(), QImage.Format.Format_ARGB32)
            combined_image.fill(Qt.GlobalColor.transparent)

            painter = QPainter(combined_image)
            painter.drawImage(0, 0, self.mask)
            painter.end()

            options = QFileDialog.Option(0)
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Save Masked Image", "", "PNG Files (*.png)", options=options
            )
            if file_name:
                combined_image.save(file_name, "PNG")

    def clear_mask(self):
        if self.mask:
            self.mask.fill(Qt.GlobalColor.transparent)
            self.image_label.setPixmap(QPixmap.fromImage(self.image))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DalleMask()
    window.show()
    sys.exit(app.exec())
