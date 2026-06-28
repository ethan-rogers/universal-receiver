import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QStyle
from PyQt6.QtGui import  QIcon, QPixmap, QPainter, QColor
from PyQt6.QtCore import pyqtSlot, Qt, QSize
from PyQt6.QtGui import QFont

import keyboard as kb

def window():
    app = QApplication(sys.argv)
    widget = QWidget()
    widget.resize(800, 400)
    widget.setWindowTitle("Reciever Mapper")

    keyboard_setup(widget)

    widget.show()
    sys.exit(app.exec())

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
    # 1. Extract a clear pixmap from the original standard icon
    original_pixmap = icon.pixmap(QSize(128, 128))
    
    # 2. Create a blank canvas of the same size with an alpha channel
    recolored_pixmap = QPixmap(original_pixmap.size())
    recolored_pixmap.fill(QColor("transparent"))
    
    # 3. Paint using composition modes
    painter = QPainter(recolored_pixmap)
    
    # Draw the original icon shape first
    painter.drawPixmap(0, 0, original_pixmap)
    
    # Switch composition: Only paint where pixels already exist (the icon's stencil)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(recolored_pixmap.rect(), color)
    
    painter.end()
    
    return QIcon(recolored_pixmap)




def create_tinted_icon(pixmap):
    painter = QPainter(pixmap)

    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), QColor("#FFFFFF"))
    painter.end()
    return QIcon(pixmap)


def button_clicked(key):
    print(key, "clicked")


if __name__ == '__main__':
    window()