import urllib
from io import BytesIO
from math import trunc

from PyQt6.QtCore import QBuffer, QPoint, QRect, Qt
from PyQt6.QtGui import QImage, QPainter, QPixmap
from PyQt6.QtWidgets import (QComboBox, QFileDialog, QHBoxLayout, QLabel,
                             QLineEdit, QMessageBox, QPushButton, QScrollArea,
                             QSizePolicy, QVBoxLayout, QWidget)

from Core.images import Dalle


class GenerateImageUI:
    dalle = Dalle()

    def set_generate_image_ui(self):
        main_layout = QVBoxLayout()

        configs_layout = QHBoxLayout()

        prompt_layout = QVBoxLayout()
        prompt_label = QLabel("Prompt to generate image")
        prompt_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        prompt_label.adjustSize()
        prompt_layout.addWidget(prompt_label)
        self.prompt_image_edit = QLineEdit()
        prompt_layout.addWidget(self.prompt_image_edit)
        configs_layout.addLayout(prompt_layout)

        size_layout = QVBoxLayout()
        size_label = QLabel("Size")
        size_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        size_label.adjustSize()
        size_layout.addWidget(size_label)
        self.size_combobox = QComboBox()
        self.size_combobox.addItems(
            [
                "256x256",
                "512x512",
                "1024x1024",
                "1792x1024",
                "1024x1792",
            ]
        )
        size_layout.addWidget(self.size_combobox)
        configs_layout.addLayout(size_layout)

        quality_layout = QVBoxLayout()
        quality_label = QLabel("Quality")
        quality_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        quality_label.adjustSize()
        quality_layout.addWidget(quality_label)
        self.quality_combobox = QComboBox()
        self.quality_combobox.addItems(["standard", "hd"])
        quality_layout.addWidget(self.quality_combobox)
        configs_layout.addLayout(quality_layout)

        main_layout.addLayout(configs_layout)

        self.generate_image_button = QPushButton("Generate Image")
        self.generate_image_button.clicked.connect(self.generate_image)
        main_layout.addWidget(self.generate_image_button)

        self.save_image_button = QPushButton("Save Image")
        self.save_image_button.clicked.connect(self.save_generated_image)
        main_layout.addWidget(self.save_image_button)

        self.image_label = QLabel()
        main_layout.addWidget(self.image_label)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.image = None

    def generate_image(self):
        try:
            prompt = self.prompt_image_edit.text()
            size = str(self.size_combobox.currentText())
            quality = str(self.quality_combobox.currentText())

            image_url = self.dalle.generate_image(prompt, size, quality)
            self.image = load_image_from_url(image_url)
            self.image_label.setPixmap(QPixmap.fromImage(self.image))
        except ValueError as e:
            error_message = QMessageBox()
            error_message.setWindowTitle("Error generating image")
            error_message.setText(str(e))
            error_message.exec()

    def save_generated_image(self):
        if self.image:
            options = QFileDialog.Option(0)
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Save Image", "", "PNG Files (*.png)", options=options
            )
            if file_name:
                self.image.save(f"{file_name}.png", "PNG")


class EditImageUI:
    dalle = Dalle()

    def set_image_edit_ui(self):
        main_layout = QVBoxLayout()

        options_layout = QHBoxLayout()

        self.load_button = QPushButton("Load Image", self)
        self.load_button.clicked.connect(self.load_image)
        options_layout.addWidget(self.load_button)

        self.clear_button = QPushButton("Clear Mask", self)
        self.clear_button.clicked.connect(self.clear_mask)
        options_layout.addWidget(self.clear_button)

        self.export_button = QPushButton("Export Mask as PNG", self)
        self.export_button.clicked.connect(self.export_image)
        options_layout.addWidget(self.export_button)

        self.save_image_button = QPushButton("Save Image", self)
        self.save_image_button.clicked.connect(self.save_image)
        options_layout.addWidget(self.save_image_button)

        main_layout.addLayout(options_layout)

        configs_layout = QHBoxLayout()

        prompt_layout = QVBoxLayout()
        prompt_layout.addWidget(QLabel("Prompt"))
        self.prompt_image_edit = QLineEdit()
        prompt_layout.addWidget(self.prompt_image_edit)
        configs_layout.addLayout(prompt_layout)

        size_layout = QVBoxLayout()
        size_layout.addWidget(QLabel("Size"))
        self.size_combobox = QComboBox()
        self.size_combobox.addItems(
            [
                "256x256",
                "512x512",
                "1024x1024",
                "1792x1024",
                "1024x1792",
            ]
        )
        size_layout.addWidget(self.size_combobox)
        configs_layout.addLayout(size_layout)

        main_layout.addLayout(configs_layout)

        self.edit_image_button = QPushButton("Edit image", self)
        self.edit_image_button.clicked.connect(self.edit_image)
        main_layout.addWidget(self.edit_image_button)

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
            self.original_image = self.original_image.convertToFormat(
                QImage.Format.Format_RGBA64
            )
            self.image = self.original_image.copy()
            self.mask = self.original_image.copy()
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

    def edit_image(self):
        try:
            if self.original_image:
                prompt = self.prompt_image_edit.text()
                size = str(self.size_combobox.currentText())

                original_image_b = qimage_to_bytes(self.original_image)
                mask_image_b = qimage_to_bytes(self.mask)

                link_new_image = self.dalle.update_image(
                    prompt, original_image_b, mask_image_b, size
                )
                self.original_image = load_image_from_url(link_new_image)
                self.original_image = self.original_image.convertToFormat(
                    QImage.Format.Format_RGBA64
                )
                self.image = self.original_image.copy()
                self.mask = self.original_image.copy()
                self.image_label.setPixmap(QPixmap.fromImage(self.image))
        except ValueError as e:
            error_message = QMessageBox()
            error_message.setWindowTitle("Error generating image")
            error_message.setText(str(e))
            error_message.exec()

    def save_image(self):
        if self.original_image:
            options = QFileDialog.Option(0)
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Save Image", "", "PNG Files (*.png)", options=options
            )
            if file_name:
                self.original_image.save(f"{file_name}.png", "PNG")


def load_image_from_url(url):
    response = urllib.request.urlopen(url)
    image_data = BytesIO(response.read())
    qimage = QImage()
    qimage.loadFromData(image_data.read())
    return qimage


def qimage_to_bytes(qimage):
    buffer = QBuffer()
    buffer.open(QBuffer.OpenModeFlag.ReadWrite)
    qimage.save(buffer, "PNG")
    buffer.seek(0)
    return BytesIO(buffer.data())
