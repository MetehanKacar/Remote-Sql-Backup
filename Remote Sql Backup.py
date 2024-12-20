import mysql.connector
import os
import datetime
import time
import threading
import tkinter as tk
from tkinter import Label, Entry, Button, StringVar, filedialog, messagebox

# Tkinter kök penceresini oluştur
root = tk.Tk()
host = StringVar()
user = StringVar()
password = StringVar()
database = StringVar()
backup_dir = StringVar()
backup_interval = StringVar()  # Süreyi StringVar olarak tanımlıyoruz

# Veritabanına bağlanma
def connect_database():
    return mysql.connector.connect(
        host=host.get(),
        user=user.get(),
        password=password.get(),
        database=database.get()
    )

# Veritabanındaki tüm tabloları bulma
def get_tables(cursor):
    cursor.execute("SHOW TABLES")
    return [table[0] for table in cursor.fetchall()]

# Tablo yapısını ve verilerini SQL olarak dışa aktarma
def backup_table(cursor, table_name, backup_file):
    cursor.execute(f"SHOW CREATE TABLE {table_name}")
    create_table_stmt = cursor.fetchone()[1] + ";\n\n"

    with open(backup_file, 'a', encoding='utf-8') as f:
        f.write(f"-- Yapı: {table_name}\n")
        f.write(f"{create_table_stmt}\n")

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    if rows:
        column_names = [i[0] for i in cursor.description]
        with open(backup_file, 'a', encoding='utf-8') as f:
            f.write(f"-- Veri: {table_name}\n")
            for row in rows:
                values = ', '.join([f"'{str(val).replace('\\', '\\\\').replace('\'', '\\\'')}'" if val is not None else 'NULL' for val in row])
                f.write(f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({values});\n")
            f.write("\n")

# Tüm veritabanını yedekleme
def backup_database():
    try:
        connection = connect_database()
        cursor = connection.cursor()
        backup_file = os.path.join(backup_dir.get(), f"Yedek_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql")
        tables = get_tables(cursor)
        for table in tables:
            backup_table(cursor, table, backup_file)

        cursor.close()
        connection.close()
        messagebox.showinfo("Başarılı", f"Succesful Backup! Path: {backup_file}")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f":{err}")

# Yedekleme işlemini belirli aralıklarla yapma
def schedule_backup():
    try:
        interval = int(backup_interval.get())  # Kullanıcıdan alınan süreyi saniyeye çevir
        while True:
            backup_database()
            time.sleep(interval)
    except ValueError:
        messagebox.showerror("Error", "Enter a valid time (seconds).")

# Yedekleme işlemini başlatma
def start_backup():
    if not backup_interval.get().isdigit():
        messagebox.showerror("Error", "Enter a valid backup time.")
        return
    threading.Thread(target=schedule_backup, daemon=True).start()
    messagebox.showinfo("Başlatıldı", "Yedekleme işlemi başlatıldı.")

# Yedekleme klasörü seçimi
def select_backup_dir():
    selected_dir = filedialog.askdirectory()
    if selected_dir:
        backup_dir.set(selected_dir)

# GUI Arayüzü
root.title("Remote Sql Backup")
root.geometry("400x350")

Label(root, text="Host:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
Entry(root, textvariable=host).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Username:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
Entry(root, textvariable=user).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Password:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
Entry(root, textvariable=password, show="*").grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Database:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
Entry(root, textvariable=database).grid(row=3, column=1, padx=10, pady=5)

Label(root, text="Path:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
Entry(root, textvariable=backup_dir).grid(row=4, column=1, padx=10, pady=5)
Button(root, text="Select", command=select_backup_dir).grid(row=4, column=2, padx=10, pady=5)

Label(root, text="Backup Delay (second):").grid(row=5, column=0, padx=10, pady=5, sticky="e")
Entry(root, textvariable=backup_interval).grid(row=5, column=1, padx=10, pady=5)

Button(root, text="Backup Start", command=start_backup).grid(row=6, column=1, padx=10, pady=20)

root.mainloop()
