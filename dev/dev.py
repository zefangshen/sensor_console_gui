import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QComboBox, QLabel, QVBoxLayout, QWidget,
    QHBoxLayout
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QComboBox Example")
        self.setGeometry(100, 100, 300, 200)

        # Central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # tab layout
        tab_layout = QHBoxLayout()
        btn1 = QLabel('Label 1')
        btn1.setFixedSize(50, 50)
        btn2= QLabel('Label 1')
        btn2.setFixedSize(50, 50)
        tab_layout.addWidget(btn1)
        tab_layout.addWidget(btn2)
        
        # tool layout
        tool_layout = QHBoxLayout()
        btn3 = QLabel('Label 3')
        btn4= QLabel('Label 4')
        tool_layout.addWidget(btn3)
        tool_layout.addWidget(btn4)

        layout.addLayout(tab_layout)
        layout.addLayout(tool_layout)

        # # Create a QComboBox
        # self.combo_box = QComboBox()
        # self.combo_box.addItems(["Apple", "Banana", "Cherry", "Date"])
        
        # # Label to display selected item
        # # self.label = QLabel("Select a fruit")
        
        # # Connect the combo box selection change signal to a method
        # self.combo_box.currentIndexChanged.connect(self.on_combobox_changed)
        
        # # Add widgets to layout
        # layout.addWidget(self.combo_box)

    def on_combobox_changed(self, index):
        selected_item = self.sender().itemText(index)
        print(f"Selected item: {selected_item}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
