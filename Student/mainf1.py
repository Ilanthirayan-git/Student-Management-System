import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3


BG_COLOR = "#f0f4f7"
TITLE_BG = "#2e86c1"
TITLE_FG = "#ffffff"
BUTTON_BG = "#3498db"
BUTTON_FG = "#ffffff"
ENTRY_BG = "#ffffff"


win = tk.Tk()
win.title("Student Management System")
win.geometry("1000x600")
win.config(bg=BG_COLOR)


conn = sqlite3.connect('student_management.db')
c = conn.cursor()


TABLE_NAME = "students_v2"

c.execute(f'''
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        roll_no TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        gender TEXT,
        contact TEXT,
        dob TEXT,
        address TEXT
    )
''')
conn.commit()


def display_students(filtered_rows=None):
    for row in tree.get_children():
        tree.delete(row)
    if filtered_rows:
        for row in filtered_rows:
            tree.insert('', 'end', values=row)
    else:
        c.execute(f"SELECT * FROM {TABLE_NAME}")
        for row in c.fetchall():
            tree.insert('', 'end', values=row)

def add_student():
    data = (
        roll_no_entry.get(),
        name_entry.get(),
        email_entry.get(),
        gender_var.get(),
        contact_entry.get(),
        dob_entry.get(),
        address_entry.get()
    )
    if "" in data:
        messagebox.showwarning("Missing Fields", "Please fill in all fields")
        return
    try:
        c.execute(f'INSERT INTO {TABLE_NAME} VALUES (?, ?, ?, ?, ?, ?, ?)', data)
        conn.commit()
        display_students()
        clear_fields()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Roll Number already exists!")

def update_student():
    data = (
        name_entry.get(),
        email_entry.get(),
        gender_var.get(),
        contact_entry.get(),
        dob_entry.get(),
        address_entry.get(),
        roll_no_entry.get()
    )
    if "" in data:
        messagebox.showwarning("Missing Fields", "Please fill in all fields")
        return
    c.execute(f'''
        UPDATE {TABLE_NAME} SET
        name=?, email=?, gender=?, contact=?, dob=?, address=?
        WHERE roll_no=?
    ''', data)
    conn.commit()
    display_students()
    clear_fields()

def delete_student():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Select a student to delete")
        return
    roll_no = tree.item(selected[0])['values'][0]
    c.execute(f'DELETE FROM {TABLE_NAME} WHERE roll_no = ?', (roll_no,))
    conn.commit()
    display_students()
    clear_fields()

def clear_fields():
    for entry in [roll_no_entry, name_entry, email_entry, contact_entry, dob_entry, address_entry]:
        entry.delete(0, tk.END)
    gender_var.set('')

def select_student(event):
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0], 'values')
        roll_no_entry.delete(0, tk.END)
        roll_no_entry.insert(0, values[0])
        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])
        email_entry.delete(0, tk.END)
        email_entry.insert(0, values[2])
        gender_var.set(values[3])
        contact_entry.delete(0, tk.END)
        contact_entry.insert(0, values[4])
        dob_entry.delete(0, tk.END)
        dob_entry.insert(0, values[5])
        address_entry.delete(0, tk.END)
        address_entry.insert(0, values[6])


tk.Label(win, text="Student Management System", font=("Arial", 24, "bold"),
         bg=TITLE_BG, fg=TITLE_FG, pady=12).pack(fill=tk.X)

form_frame = tk.Frame(win, bg=BG_COLOR, padx=20, pady=20)
form_frame.place(x=20, y=80)

labels = ["Roll No", "Name", "Email", "Gender", "Contact", "Date of Birth", "Address"]

for i, label in enumerate(labels):
    tk.Label(form_frame, text=label, font=("Arial", 12), bg=BG_COLOR).grid(row=i, column=0, sticky='w', pady=5)

roll_no_entry = tk.Entry(form_frame, bg=ENTRY_BG)
name_entry = tk.Entry(form_frame, bg=ENTRY_BG)
email_entry = tk.Entry(form_frame, bg=ENTRY_BG)
gender_var = tk.StringVar()
gender_combo = ttk.Combobox(form_frame, textvariable=gender_var, values=["Male", "Female"], state="readonly")
contact_entry = tk.Entry(form_frame, bg=ENTRY_BG)
dob_entry = tk.Entry(form_frame, bg=ENTRY_BG)
address_entry = tk.Entry(form_frame, bg=ENTRY_BG)

widgets = [
    roll_no_entry, name_entry, email_entry,
    gender_combo, contact_entry, dob_entry, address_entry
]

for i, entry in enumerate(widgets):
    entry.grid(row=i, column=1, pady=5, padx=10)


button_frame = tk.Frame(win, bg=BG_COLOR)
button_frame.place(x=320, y=80)

def styled_button(parent, text, cmd, row):
    return tk.Button(parent, text=text, width=12, font=("Arial", 10, "bold"),
                     bg=BUTTON_BG, fg=BUTTON_FG, command=cmd).grid(row=row, column=0, pady=5)

styled_button(button_frame, "Add", add_student, 0)
styled_button(button_frame, "Update", update_student, 1)
styled_button(button_frame, "Delete", delete_student, 2)
styled_button(button_frame, "Clear", clear_fields, 3)


table_frame = tk.Frame(win, bg=BG_COLOR)
table_frame.place(x=460, y=80, width=510, height=480)

scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
tree = ttk.Treeview(table_frame, columns=("Roll No", "Name", "Email", "Gender", "Contact", "DOB", "Address"),
                    show='headings', yscrollcommand=scroll_y.set)
scroll_y.config(command=tree.yview)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
tree.pack(fill=tk.BOTH, expand=True)

for col in ("Roll No", "Name", "Email", "Gender", "Contact", "DOB", "Address"):
    tree.heading(col, text=col)
    tree.column(col, anchor='center', width=100)

tree.bind("<ButtonRelease-1>", select_student)


display_students()
win.mainloop()
conn.close()
