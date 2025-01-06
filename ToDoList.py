import sys
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
import sqlite3

class ToDoDatabase:
    def __init__(self, db_name = "ToDo's.db"):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        todo TEXT NOT NULL
        )   
        """)
        self.con.commit()

    def add_ToDo(self, task):
        self.cur.execute(
        "INSERT INTO todos (todo) VALUES (?)",
            (task,)
        )
        self.con.commit()

    def remove_ToDo(self, task):
        self.cur.execute(
            "DELETE FROM todos WHERE todo = ?",
            (task,)
        )
        self.con.commit()

    def list_ToDos(self):
        self.cur.execute("SELECT * FROM todos")
        todoListings = self.cur.fetchall()
        if not todoListings:
            print("No To Do's")
        else:
            for i in todoListings:
                print(f"{i[1]}")

    def close_table(self):
        self.con.close()

    def clear_table(self):
        self.cur.execute("DELETE FROM todos")
        self.con.commit()

class ToDoList(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db #database whatever ion even understand ts rn
        self.settings()
        self.layout()
        self.load_items()

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
            self.db.add_ToDo(text)
            self.adder.clear()
        if self.itemlists.count() > 0:
            self.clear_button.setEnabled(True)
        else:
            self.clear_button.setEnabled(False)

    def removeItems(self):
        selected_item = self.itemlists.currentRow()
        text = self.itemlists.item(selected_item).text().strip()
        self.itemlists.takeItem(selected_item)
        self.db.remove_ToDo(text)
        self.itemlists.itemClicked.connect(self.rise_and_shine)

        if self.itemlists.count() > 0:
            self.clear_button.setEnabled(True)
        else:
            self.clear_button.setEnabled(False)

    def clearItems(self):
        self.itemlists.clear()
        self.clear_button.setEnabled(False)
        self.db.clear_table()

    def rise_and_shine(self):
        self.remove_button.setEnabled(True)

    def load_items(self):
        self.db.cur.execute("SELECT * FROM todos")
        todos = self.db.cur.fetchall()
        for todo in todos:
            self.itemlists.addItem(todo[1])




def main():
    # create instance of the database
    db = ToDoDatabase()

    app = QApplication(sys.argv)

    # create main window
    window = ToDoList(db)
    window.show()

    # execute the application
    app.exec()

    db.list_ToDos()
    db.close_table()


if __name__ == "__main__":
    main()
