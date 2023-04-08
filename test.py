import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        # metin kutusu
        self.textbox = QLineEdit(self)
        vbox.addWidget(self.textbox)

        # tuş takımı
        hbox = QHBoxLayout()
        for i in range(10):
            button = QPushButton(str(i), self)
            button.clicked.connect(self.buttonClicked)
            hbox.addWidget(button)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.setWindowTitle('Tuş Takımı ve Metin Kutusu')

        # arka plan rengini beyaz yap
        self.setStyleSheet("background-color: white;")

        # tuş takımı ve metin kutusu arasındaki mesafeyi artır
        vbox.setSpacing(20)

    def buttonClicked(self):
        sender = self.sender()
        digit = sender.text()
        self.textbox.insert(digit)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.showFullScreen()
    sys.exit(app.exec_())
