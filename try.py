import customtkinter as ctk
from tkinter import filedialog
import csv
import mysql.connector
import json
ctk.set_appearance_mode('system')
ctk.set_default_color_theme('blue')

class FirstModule(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FirstModule")
        self.geometry("400x200")

        self.dbconfig   =   {
            'host': 'localhost',
            'user': 'Admin',
            'password': 'admin'
        }
        self.dbname = 'Users'

        self.init_database()

        ctk.CTkLabel(self,text  = "First Module task").pack(pady=10)

        ctk.CTkButton(self, text = "Import", command = self.import_file).pack(pady=15)
        ctk.CTkButton(self, text = "Export", command = self.export_file).pack(pady=15)
    def init_database(self):
        try:
            # Шаг 1: подключение без базы
            conn = mysql.connector.connect(**self.dbconfig)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.dbname}")
            conn.commit()
            conn.close()

            # Шаг 2: подключение с базой
            self.conn = mysql.connector.connect(**self.dbconfig, database=self.dbname)
            self.cursor = self.conn.cursor()

            # Шаг 3: создаём таблицу
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS FirstModule(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    email VARCHAR(255),
                    role VARCHAR(255)
                )
            """)
            self.conn.commit()

        except mysql.connector.Error as err:
            print("Ошибка MySQL:", err)
            self.destroy()


    def import_file(self):
        pathfinder = filedialog.askopenfilename(filetypes=[('CSV','*.csv')])

        if not pathfinder:
            return
        try:
            with open(pathfinder,'r',encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.cursor.execute(
                        "INSERT INTO FirstModule (name, email, role) VALUES (%s,%s,%s)",
                        (row['name'],row['email'], row['role'])
                    )
                self.conn.commit()
            print("Success!")
        except Exception as e:
            print(e)

    def export_file(self):
        pathfinder = filedialog.asksaveasfilename(defaultextension='.csv',filetypes=[('CSV','*.csv')])

        if not pathfinder:
            return
        try:
            self.cursor.execute("SELECT name, email, role FROM FirstModule")
            rows = self.cursor.fetchall()
            with open(pathfinder,'w',newline='',encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(['name', 'email', 'role'])
                writer.writerows(rows)
            print("Success!")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    app = FirstModule()
    app.mainloop()