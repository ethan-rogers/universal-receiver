import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QStyle, QLabel, QTableWidget, QAbstractItemView
from PyQt6.QtGui import  QIcon, QPixmap, QPainter, QColor
from PyQt6.QtCore import pyqtSlot, Qt, QSize
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QRunnable, QThreadPool, QTimer, pyqtSlot


import keyboard as kb

from receiver import Receiver
from mappings import Mapping

mapper = Mapping()
arduino = Receiver(mapper)

threadpool = QThreadPool()

def window():
    app = QApplication(sys.argv)
    widget = QWidget()
    widget.resize(800, 400)
    widget.setWindowTitle("Reciever Mapper")


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
    arduino.conenct()

    if (arduino.get_port() == None):
        text.setText("Connection Failed")
        button.setEnabled(True)
    else:
        text.setText(f"Connected ({arduino.get_port()})")
        button.setEnabled(False)

        threadpool.start(arduino)


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
                    if "png" not in k:
                        pixmapi = getattr(QStyle.StandardPixmap, k)
                        icon = widget.style().standardIcon(pixmapi)
                        recolored_icon = recolor_icon(icon, QColor("white"))
                        button.setIcon(recolored_icon)
                    else:
                        icon_path = f"icons/{k}"
                        icon = QIcon(icon_path)
                        recolored_icon = recolor_icon(icon, QColor("white"))
                        button.setIcon(recolored_icon)
                else:
                    button.setFont(font)
                    button.setText(k)
                button.clicked.connect(lambda checked, k=k : mapper.add_key(k))

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

def command(widget):
    table = QTableWidget(1, 2, widget)
    table.move(23, 280)
    table.resize(480, 30)

    table.setColumnWidth(0, 238)
    table.setColumnWidth(1, 238)
    table.verticalHeader().setVisible(False)
    table.horizontalHeader().setVisible(False)
    table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

    mapper.set_command(table)

    add_button = QPushButton(widget)
    add_button.setGeometry(23, 320, 40, 30)
    add_button.setText("Add")
    add_button.clicked.connect(mapper.add_mapping)

    remove_key_button = QPushButton(widget)
    remove_key_button.setGeometry(73, 320, 40, 30)
    remove_key_button.setText("-")
    remove_key_button.clicked.connect(mapper.remove_key)


    clear_button = QPushButton(widget)
    clear_button.setGeometry(123, 320, 60, 30)
    clear_button.setText("Clear")
    clear_button.clicked.connect(mapper.clear)


def mapping_table(widget):
    table = QTableWidget(8, 2, widget)
    table.move(520, 60)
    table.resize(220, 250)

    table.setColumnWidth(0, 108)
    table.setColumnWidth(1, 108)
    table.verticalHeader().setVisible(False)
    table.horizontalHeader().setVisible(False)

    table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

    mapper.set_table(table)

    for i in range(8):
        button = QPushButton(widget)
        button.setGeometry(750, 65 + i*30, 30, 30)
        button.setText("-")
        button.clicked.connect(lambda x, index = i : mapper.remove_mapping(index))

    button = QPushButton(widget)
    button.setText("Map")
    button.setGeometry(520, 320, 80, 30)
    button.clicked.connect(lambda x : mapper.map_to_arduino)


if __name__ == '__main__':
    window()