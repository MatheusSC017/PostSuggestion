from io import BytesIO
from math import trunc

from PyQt6.QtCore import QBuffer, QPoint, QRect, Qt
from PyQt6.QtGui import QImage, QPainter, QPixmap
from PyQt6.QtWidgets import (QFileDialog, QLabel, QPushButton, QScrollArea,
                             QVBoxLayout, QWidget, QLineEdit)

from Core.images import Dalle


class DalleMaskUI:
    dalle = Dalle()

    def set_dalle_mask_ui(self):
        main_layout = QVBoxLayout()

        self.load_button = QPushButton("Load Image", self)
        self.load_button.clicked.connect(self.load_image)
        main_layout.addWidget(self.load_button)

        self.clear_button = QPushButton("Clear Mask", self)
        self.clear_button.clicked.connect(self.clear_mask)
        main_layout.addWidget(self.clear_button)

        self.export_button = QPushButton("Export Mask as PNG", self)
        self.export_button.clicked.connect(self.export_image)
        main_layout.addWidget(self.export_button)

        main_layout.addWidget(QLabel("Prompt"))
        self.prompt_image = QLineEdit()
        main_layout.addWidget(self.prompt_image)
        self.edit_image = QPushButton("Edit image", self)
        self.edit_image.clicked.connect(self.edit_image_dalle)
        main_layout.addWidget(self.edit_image)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_image = QScrollArea()
        scroll_image.setWidget(self.image_label)
        scroll_image.setWidgetResizable(True)
        main_layout.addWidget(scroll_image)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.original_image = None
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
            self.original_image = QImage(file_name)
            self.image = QImage(file_name)
            self.mask = QImage(file_name)
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
            self.paint_rectangle(self.image, False)
            self.paint_rectangle(self.mask, True)

            combined_image = QImage(self.image.size(), QImage.Format.Format_ARGB32)
            painter = QPainter(combined_image)
            painter.drawImage(0, 0, self.image)
            painter.drawImage(0, 0, self.mask)
            painter.end()

            self.image_label.setPixmap(QPixmap.fromImage(combined_image))

    def paint_rectangle(self, image, transparent):
        painter = QPainter(image)
        if transparent:
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.setPen(Qt.GlobalColor.transparent)
            painter.setBrush(Qt.GlobalColor.transparent)
        else:
            painter.setPen(Qt.GlobalColor.white)
            painter.setBrush(Qt.GlobalColor.white)

        rect = QRect(self.selection_start, self.selection_end).normalized()
        painter.drawRect(rect)
        painter.end()

    def export_image(self):
        if self.image and self.mask:
            options = QFileDialog.Option(0)
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Save Masked Image", "", "PNG Files (*.png)", options=options
            )
            if file_name:
                self.mask.save(f"{file_name}.png", "PNG")

    def clear_mask(self):
        if self.mask:
            self.mask = self.original_image.copy()
            self.image = self.original_image.copy()

            self.image_label.setPixmap(QPixmap.fromImage(self.image))

    def edit_image_dalle(self):
        prompt = self.prompt_image.text()

        if len(prompt) < 10:
            raise ValueError(
                "Prompt text must contain at least 10 characters"
            )

        original_image_b = self.qimage_to_bytes(self.original_image)
        mask_image_b = self.qimage_to_bytes(self.mask)

        self.dalle.update_image(prompt, original_image_b, mask_image_b)

    @staticmethod
    def qimage_to_bytes(qimage):
        buffer = QBuffer()
        buffer.open(QBuffer.OpenModeFlag.ReadWrite)
        qimage.save(buffer, "PNG")
        buffer.seek(0)
        return BytesIO(buffer.data())
