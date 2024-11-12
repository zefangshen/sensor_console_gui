from PyQt6.QtWidgets import QApplication
from app.main_window import MainWindow
from PyQt6.QtGui import QIcon
from ipdb import set_trace

if __name__ == '__main__': 
    import sys

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('./resources/images/spectra.png'))

    # read style file
    with open('resources/styles/global.css') as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
