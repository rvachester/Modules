import customtkinter as ctk
import mysql.connector
import csv
from tkinter import filedialog

ctk.set_appearance_mode('system')
ctk.set_default_color_theme('blue')

class App(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("FirstModule")
        self.geometry('400x200')

        self.dbconfig = {
            'host': "localhost",
            'user': "Admin",
            'password': "admin"
        }
        self.dbname = "Users"

        self.db_init()

        ctk.CTkLabel(self, text= "Start").pack(pady = 10)
        ctk.CTkButton(self, text= 'Import',command= self.import_file).pack(pady=15)
        ctk.CTkButton(self, text= 'Export',command= self.export_file).pack(pady=15)

    def db_init(self):
        try:
            conn = mysql.connector.connect(**self.dbconfig)
            cursor = conn.cursor()
            cursor.execute (F"CREATE DATABASE IF NOT EXISTS {self.dbname}")
            conn.commit()
            conn.close()
            
            self.conn = mysql.connector.connect(**self.dbconfig, database = self.dbname)
            self.cursor = self.conn.cursor()

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    email VARCHAR(255),
                    role VARCHAR(255)                        
                    )
            """)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.destroy()
    
    def import_file(self):
        path = filedialog.askopenfilename(filetypes=[('CSV','*.csv')])
        if not path: return
        try:
            with open(path,'r',encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.cursor.execute("INSERT INTO users (name, email, role) VALUES (%s, %s, %s)",
                                        (row['name'], row['email'], row['role'])
                                        )
                    self.conn.commit()
            print("Success")
        except Exception as e:
            print(e)

    def export_file(self):
        path = filedialog.askopenfilename(filetypes=[('CSV','*.csv')])
        if not path: return
        try:
            self.cursor.execute('SELECT name, email, role FROM users')
            rows = self.cursor.fetchall()
            with open(path,'w',newline='',encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                writer.writerow(['name','email', 'role'])
                writer.writerows(rows)
            print("Success")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    app = App()
    app.mainloop()