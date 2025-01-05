import sys
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget

class ToDoList(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.layout()

    #settings
    def settings(self):
        self.setWindowTitle("Lil Vinny To Do List")
        self.setGeometry(500, 200, 500, 500)

    #design
    def layout(self):

        #creating the buttons and shiz
        self.title = QLabel("")
        self.itemlists = QListWidget()
        self.add_button = QPushButton("Add Item")
        self.remove_button = QPushButton("Remove Item")
        self.clear_button = QPushButton("Clear Items")
        self.adder = QLineEdit()

        # creating the layout
        self.main_layout = QVBoxLayout()
        row = QHBoxLayout()

        row.addWidget(self.add_button)
        row.addWidget(self.remove_button)
        row.addWidget(self.clear_button)

        #putting it all together

        self.main_layout.addWidget(self.adder)
        self.main_layout.addLayout(row)
        self.main_layout.addWidget(self.itemlists)
        self.setLayout(self.main_layout)

        #disable clear and remove on start
        self.remove_button.setEnabled(False)
        self.clear_button.setEnabled(False)

        self.add_button.clicked.connect(self.addItem)
        self.remove_button.clicked.connect(self.removeItems)
        self.clear_button.clicked.connect(self.clearItems)
        self.adder.returnPressed.connect(self.addItem)
        self.itemlists.itemClicked.connect(self.rise_and_shine)

    def addItem(self):
        text = self.adder.text().strip()
        if text:
            self.itemlists.addItem(text)
            self.adder.clear()
        if self.itemlists.count() > 0:
            self.clear_button.setEnabled(True)
        else:
            self.clear_button.setEnabled(False)

    def removeItems(self):
        selected_item = self.itemlists.currentRow()
        self.itemlists.takeItem(selected_item)

        if self.itemlists.count() > 0:
            self.clear_button.setEnabled(True)
        else:
            self.clear_button.setEnabled(False)

    def clearItems(self):
        self.itemlists.clear()
        self.clear_button.setEnabled(False)

    def rise_and_shine(self):
        self.remove_button.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    window = ToDoList()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
