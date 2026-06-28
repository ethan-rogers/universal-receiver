import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QFont

import keyboard as kb

def window():
    app = QApplication(sys.argv)
    widget = QWidget()
    widget.resize(800, 400)
    widget.setWindowTitle("Reciever Mapper")

    font = QFont("Arial", 7) 
    x_pos, y_pos = kb.top_left

    for rows in kb.rows:
        keys = rows[0]
        width = rows[1]

        for i, k in enumerate(keys):

            if k != "na":
                button = QPushButton(widget)
                button.setFont(font)
                button.setText(k)
                button.setGeometry(x_pos, y_pos, width[i], kb.height)
                button.clicked.connect(lambda checked, k=k : button_clicked(k))

            x_pos += kb.spacing + width[i]

        x_pos = kb.top_left[0]
        y_pos += kb.height + kb.spacing




    widget.show()
    sys.exit(app.exec())


def button_clicked(key):
    print(key, "clicked")


if __name__ == '__main__':
    window()