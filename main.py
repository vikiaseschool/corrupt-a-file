import os
import random
import subprocess
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QStandardPaths


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Corrupt a File! by @vikiase")
        self.setWindowState(Qt.WindowState.WindowMaximized)
        self.setStyleSheet("background-color: black;")

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Zarovnání na střed

        self.header_label = QLabel("Too late to do your homework?", self)
        self.header_label.setStyleSheet("color: red; font-size: 24px;")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.corrupt_file_button = QPushButton("Corrupt a File!", self)
        self.corrupt_file_button.setStyleSheet("background-color: white; color: black; font-size: 16px;")
        self.corrupt_file_button.setFixedHeight(50)  # Normální výška tlačítka
        self.corrupt_file_button.clicked.connect(self.show_file_options)

        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap("skull.jpg").scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.format_buttons_layout = QHBoxLayout()
        self.pdf_button = QPushButton("PDF", self)
        self.docx_button = QPushButton("DOCX", self)
        self.pptx_button = QPushButton("PPTX", self)
        self.xls_button = QPushButton("XLS", self)

        for button in [self.pdf_button, self.docx_button, self.pptx_button, self.xls_button]:
            button.setStyleSheet("background-color: white; color: black; font-size: 16px;")
            button.setFixedHeight(50)
            button.setVisible(False)
            self.format_buttons_layout.addWidget(button)

        self.exit_button = QPushButton("I am scared.", self)
        self.exit_button.setStyleSheet("background-color: white; color: black; font-size: 16px;")
        self.exit_button.setFixedHeight(50)
        self.exit_button.setVisible(False)
        self.exit_button.clicked.connect(self.exit_application)

        main_layout.addWidget(self.header_label)
        main_layout.addWidget(self.corrupt_file_button)
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(self.format_buttons_layout)
        main_layout.addWidget(self.exit_button)

        self.setLayout(main_layout)

        self.created_file = None

        self.pdf_button.clicked.connect(lambda: self.create_and_corrupt_file("pdf"))
        self.docx_button.clicked.connect(lambda: self.create_and_corrupt_file("docx"))
        self.pptx_button.clicked.connect(lambda: self.create_and_corrupt_file("pptx"))
        self.xls_button.clicked.connect(lambda: self.create_and_corrupt_file("xls"))

    def show_file_options(self):
        for button in [self.pdf_button, self.docx_button, self.pptx_button, self.xls_button]:
            button.setVisible(True)
        self.corrupt_file_button.setVisible(False)

    def create_and_corrupt_file(self, file_format):
        downloads_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation)
        file_path = os.path.join(downloads_path, f"corrupted_file.{file_format}")
        with open(file_path, "w") as file:
            file.write(f"This is a test {file_format.upper()} file.\n")
            file.write(f"Tec{file_format.upper()}hnology has {file_format.upper()}become an integra{file_format.upper()}l part of our da{file_format.upper()}ily lives. It enhances communication, simplifies tasks, and {file_format.upper()}boosts productivity. However, with its development come {file_format.upper()}challenges, such as privacy protection and cybersecurity. It is crucial to find a balance betweenleveraging te{file_format.upper()}chnology and safeguarding personal rights and freedoms.")

        with open(file_path, "r+b") as file:
            data = file.read()
            print(len(data))
            file.seek(5)
            file.write(bytearray(random.getrandbits(8) for _ in range(len(data))))

        self.created_file = file_path
        print(f"Soubor vytvořen a poškozen: {file_path}")

        self.exit_button.setVisible(True)

        self.show_success_dialog()

    def show_success_dialog(self):
        if not self.created_file:
            return

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Corruption successful")
        msg_box.setText("The file was corrupted.\nYou are safe now.")
        msg_box.setIcon(QMessageBox.Icon.Information)

        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: black;
                font-size: 16px;
            }
            QMessageBox QLabel {
                color: red;  /* Červený text */
            }
            QMessageBox QPushButton {
                background-color: white;
                color: black;
            }
        """)

        open_button = msg_box.addButton("Go to file", QMessageBox.ButtonRole.AcceptRole)
        cancel_button = msg_box.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)

        msg_box.exec()

        if msg_box.clickedButton() == open_button:
            self.open_file_location()

    def open_file_location(self):
        if self.created_file:
            file_path = os.path.normpath(self.created_file)
            if os.name == "nt":  # Windows
                subprocess.Popen(f'start "" "{file_path}"', shell=True)
            elif os.name == "posix":  # macOS/Linux
                subprocess.Popen(["xdg-open", file_path])

    def exit_application(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
