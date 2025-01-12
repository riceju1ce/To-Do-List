import sys
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget,QCalendarWidget
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QDate, Qt
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
        self.remove_button = QPushButton("Remove Task")
        self.clear_button = QPushButton("Clear Tasks")
        self.dialog = QPushButton("Add Task")

        # creating the layout
        self.main_layout = QVBoxLayout()
        row = QHBoxLayout()

        row.addWidget(self.dialog)
        row.addWidget(self.remove_button)
        row.addWidget(self.clear_button)

        #putting it all together
        self.main_layout.addLayout(row)
        self.main_layout.addWidget(self.itemlists)

        #disable clear and remove on start
        self.remove_button.setEnabled(False)
        self.clear_button.setEnabled(False)

        self.remove_button.clicked.connect(self.removeItems)
        self.clear_button.clicked.connect(self.clearItems)
        self.itemlists.itemClicked.connect(self.rise_and_shine)
        self.dialog.clicked.connect(self.dialog_box)

        self.setLayout(self.main_layout)

    def removeItems(self):
        selected_item = self.itemlists.currentRow()
        text = self.itemlists.item(selected_item).text().strip()
        self.itemlists.takeItem(selected_item)
        self.db.remove_ToDo(text)

        if self.itemlists.count() > 0:
            self.clear_button.setEnabled(True)
            self.remove_button.setEnabled(True)
        else:
            self.clear_button.setEnabled(False)
            self.remove_button.setEnabled(False)
    def clearItems(self):
        self.itemlists.clear()
        self.clear_button.setEnabled(False)
        self.db.clear_table()
        self.clear_button.setEnabled(False)
        self.remove_button.setEnabled(False)

    def rise_and_shine(self):
        self.remove_button.setEnabled(True)

    def load_items(self):
        self.db.cur.execute("SELECT * FROM todos")
        todos = self.db.cur.fetchall()
        for todo in todos:
            self.itemlists.addItem(todo[1])

    def dialog_box(self):
        self.msg = QDialog()
        self.msg.setWindowTitle("dialog box")
        self.msg.show()
        
        # formatting
        self.titleText = QLabel("Title")
        self.titleEdit = QLineEdit()
        self.titleEdit.setPlaceholderText("Task Title")
        self.dateSelect = QCalendarWidget()
        self.dateSelect.showToday()
        current_Date = QDate.currentDate()
        self.dateSelect.setMinimumDate(current_Date)
        self.descText = QLabel("Description")
        self.descEdit = QLineEdit("")
        self.descEdit.setPlaceholderText("Description of Task")
        self.DialogAddTask = QPushButton("Save")
        self.DialogCancelTask = QPushButton("Cancel")
        self.dueDateLabel = QLabel("Due Date")

        layout = QVBoxLayout()
        layout.addWidget(self.titleText)
        layout.addWidget(self.titleEdit)
        layout.addWidget(self.dueDateLabel)
        layout.addWidget(self.dateSelect)
        layout.addWidget(self.descText)
        layout.addWidget(self.descEdit)
        layout.addWidget(self.DialogAddTask)
        layout.addWidget(self.DialogCancelTask)

        self.msg.setLayout(layout)

        self.DialogAddTask.clicked.connect(self.addTask)
        self.DialogCancelTask.clicked.connect(self.cancelTask)
        self.titleEdit.editingFinished.connect(self.edit_made)
        self.titleEdit.returnPressed.connect(self.edit_made)
        self.DialogAddTask.setEnabled(False)



    def edit_made(self):
        blob = self.titleEdit.text().strip()
        if blob == "":
            self.DialogAddTask.setEnabled(False)
        else:
            self.DialogAddTask.setEnabled(True)

    def addTask(self):

        text = self.titleEdit.text().strip()
        moretext = self.descEdit.text().strip()

        date = self.dateSelect.selectedDate()

        today_Date = QDate.currentDate()

        if date.year() == today_Date.year():
            DueDateText = f"Due {date.toString('dddd, MMM d')}"
        else: DueDateText = f"Due {date.toString('dddd, MMM d yyyy')}"

        days_diff = today_Date.daysTo(date)

        if days_diff == 0:
            remaining = "Today"
        elif days_diff == 1:
            remaining = "Tomorrow"
        elif days_diff == -1:
            remaining = "Yesterday"
        elif days_diff > 1:
            remaining = f"In {days_diff} days"
        else:
            remaining = f"{days_diff} days ago"

        if text:
            self.widget = QWidget()
            layout = QVBoxLayout()
            taskTitle = QLabel(text)

            if moretext:
                taskDesc = QLabel(moretext)
                layout.addWidget(taskDesc)

            taskDate = QLabel(DueDateText)

            daysUntil = QLabel(remaining)

            font = QFont()
            font.setBold(True)
            taskTitle.setFont(font)

            taskDate.setAlignment(Qt.AlignmentFlag.AlignLeft)

            daysUntil.setAlignment(Qt.AlignmentFlag.AlignRight)

            layout.addWidget(taskTitle)

            item = QWidget()
            layout2 = QHBoxLayout()
            layout2.setContentsMargins(0, 0, 0, 0)


            layout2.addWidget(taskDate)
            layout2.addWidget(daysUntil)

            item.setLayout(layout2)

            layout.addWidget(item)

            self.widget.setLayout(layout)

            # adding the widget to the list
            item = QListWidgetItem(self.itemlists)
            item.setSizeHint(self.widget.sizeHint())
            self.itemlists.setItemWidget(item, self.widget)
            self.msg.close()


        if self.itemlists.count() > 0:
            self.clear_button.setEnabled(True)
        else:
            self.clear_button.setEnabled(False)

    def cancelTask(self):
        self.msg.close()

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

# to do:
# add check box next to tasks for when you complete them
# after u check it becomes gray
# connect to db
# add a visual timeline bar
# improve ui
