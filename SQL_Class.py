import sqlite3
from tkinter import END


class SQLDealer:
    def __init__(self):
        self.hello = "world"

    def create_sent_gmail(self):
        conn = sqlite3.connect("./sent_box/sent.db")
        curr = conn.cursor()
        curr.execute('''CREATE TABLE IF NOT EXISTS sent_gmail(
            receiver text,
            subject text,
            type text,
            time text
        )''')
        conn.commit()
        conn.close()

    def create_gmail_text(self):
        conn = sqlite3.connect("./sent_box/sent.db")
        curr = conn.cursor()
        curr.execute('''CREATE TABLE IF NOT EXISTS gmail_text(
            time text,
            actual_text text
        )''')
        conn.commit()
        conn.close()

    def insert_data(self, receiver, subject, letter_type, sent_time, actual_text):
        conn = sqlite3.connect("./sent_box/sent.db")
        curr = conn.cursor()
        curr.execute(f'''INSERT INTO sent_gmail(receiver, subject, type, time)
                        VALUES ('{receiver}', '{subject}', '{letter_type}', '{sent_time}');
                        ''')
        curr.execute(f"INSERT INTO gmail_text(time, actual_text) VALUES('{sent_time}', '{actual_text}');")
        conn.commit()
        conn.close()

    def display_data(self, table):
        conn = sqlite3.connect("./sent_box/sent.db")
        curr = conn.cursor()
        gmail = curr.execute('''SELECT * FROM sent_gmail;''').fetchall()
        if len(gmail) > 0:
            table.delete(*table.get_children())
            for email in gmail:
                table.insert("", END, values=email)
        conn.commit()
        conn.close()

    def return_wanted_text(self, exact_time):
        conn = sqlite3.connect("./sent_box/sent.db")
        curr = conn.cursor()
        wanted = [list(item) for item in curr.execute(f"SELECT actual_text FROM gmail_text "
                                                      f"WHERE time = '{exact_time}'")]
        result = wanted[0][0]
        conn.commit()
        conn.close()
        return result

    def delete_sent_data(self):
        conn = sqlite3.connect("./sent_box/sent.db")
        curr = conn.cursor()
        curr.execute('''DELETE FROM sent_gmail;''')
        curr.execute('''DELETE FROM gmail_text;''')
        conn.commit()
        conn.close()
