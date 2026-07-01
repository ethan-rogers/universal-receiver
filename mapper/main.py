import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QStyle, QLabel, QTableWidget, QAbstractItemView
from PyQt6.QtGui import  QIcon, QPixmap, QPainter, QColor
from PyQt6.QtCore import pyqtSlot, Qt, QSize
from PyQt6.QtGui import QFont

import keyboard as kb
import receiver


arduino = None

def window():
    app = QApplication(sys.argv)
    widget = QWidget()
    widget.resize(800, 400)
    widget.setWindowTitle("Reciever Mapper")

    receiver.init()

    keyboard_setup(widget)
    setup_connect(widget)
    command(widget)
    mapping_table(widget)

    widget.show()
    sys.exit(app.exec())

def setup_connect(widget):
    button = QPushButton(widget)
    button.setText("Connect")
    button.setGeometry(700, 20, 80, 30)
    button.clicked.connect(lambda x : try_connection(button, text))


    text = QLabel(widget)
    text.setText("Connection Failed")
    text.setGeometry(520, 20, 150, 30)
    text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    try_connection(button, text)


def try_connection(button, text):
    arduino = receiver.init()

    if (arduino == None):
        text.setText("Connection Failed")
        button.setEnabled(True)
    else:
        text.setText(f"Connected ({arduino.device})")
        button.setEnabled(False)

def keyboard_setup(widget):
    font = QFont("Arial", 7) 
    x_pos, y_pos = kb.top_left

    in_media = True

    for rows in kb.rows:
        keys = rows[0]
        width = rows[1]

        for i, k in enumerate(keys):

            if k != "na":
                button = QPushButton(widget)
                # row one is media buttons with icons
                if in_media:
                    pixmapi = getattr(QStyle.StandardPixmap, k)
                    icon = widget.style().standardIcon(pixmapi)
                    recolored_icon = recolor_icon(icon, QColor("white"))
                    button.setIcon(recolored_icon)
                else:
                    button.setFont(font)
                    button.setText(k)
                button.clicked.connect(lambda checked, k=k : button_clicked(k))

                button.setGeometry(x_pos, y_pos, width[i], kb.height)

            x_pos += kb.spacing + width[i]

        x_pos = kb.top_left[0]

        if in_media:
            y_pos += kb.media_buffer
        in_media = False
        y_pos += kb.height + kb.spacing


def recolor_icon(icon: QIcon, color: QColor) -> QIcon:
    original_pixmap = icon.pixmap(QSize(128, 128))
    recolored_pixmap = QPixmap(original_pixmap.size())
    recolored_pixmap.fill(QColor("transparent"))
    painter = QPainter(recolored_pixmap)

    painter.drawPixmap(0, 0, original_pixmap)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(recolored_pixmap.rect(), color)
    
    painter.end()
    
    return QIcon(recolored_pixmap)

def button_clicked(key):
    print(key, "clicked")

def command(widget):
    table = QTableWidget(1, 2, widget)
    table.move(23, 280)
    table.resize(405, 30)

    table.setColumnWidth(0, 200)
    table.setColumnWidth(1, 200)
    table.verticalHeader().setVisible(False)
    table.horizontalHeader().setVisible(False)
    table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)


    button = QPushButton(widget)
    button.setGeometry(460, 280, 40, 30)
    button.setText("Add")

def mapping_table(widget):
    table = QTableWidget(8, 2, widget)
    table.move(520, 60)
    table.resize(200, 250)

    table.setColumnWidth(0, 98)
    table.setColumnWidth(1, 98)
    table.verticalHeader().setVisible(False)
    table.horizontalHeader().setVisible(False)

    table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)



if __name__ == '__main__':
    window()