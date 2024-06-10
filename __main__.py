from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication
from loguru import logger

import sys

from app.interface import StartWindow

if __name__ == '__main__':
    logger.add(
        "logs/logs.log",
        level="DEBUG",
        format="{time} {level} {message}",
        rotation="10 MB",  # Ротация лог-файла по размеру
        compression="zip",  # Сжатие старых лог-файлов в zip-архивы
        enqueue=True,  # Записывать сообщения асинхронно
    )
    QCoreApplication.setApplicationName("Map")

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')

    capture_window = StartWindow()
    capture_window.show()
    sys.exit(app.exec_())
