import sqlite3
from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:

    # get a cursor object to execute SQL commands
    c = connection.cursor()

    # create the table
    # c.execute("""
    #     CREATE TABLE tasks(
    #     task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     name TEXT NOT NULL,
    #     due_date TEXT NOT NULL,
    #     priority INTEGER NOT NULL,
    #     status INTEGER NOT NULL)
    #     """)

    # insert dummy data into the table
    c.execute(
        'INSERT INTO tasks(name, due_date, priority, status)'
        'VALUES("Finish this tutorial", "07/16/2015", 10, 1)')

    c.execute(
        'INSERT INTO tasks(name, due_date, priority, status)'
        'VALUES("Fininsh Real Python Course 2", "09/10/2019",10, 1)')
