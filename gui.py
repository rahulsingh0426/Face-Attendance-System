import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import add_face
import mark_attendance
import database

def add_face_gui():
    name = simpledialog.askstring("Input", "Enter the name of the person:")
    if name:
        add_face.add_face(name)
        messagebox.showinfo("Info", f"Face for {name} added successfully!")

def mark_attendance_gui():
    mark_attendance.mark_attendance()

def view_attendance():
    records = database.get_attendance_records()
    attendance_window = tk.Toplevel()
    attendance_window.title("Attendance Records")
    attendance_window.geometry("400x300")
    tree = ttk.Treeview(attendance_window, columns=("Name", "Date", "Time"), show="headings")
    tree.heading("Name", text="Name")
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    for record in records:
        tree.insert("", tk.END, values=record)
    tree.pack(expand=True, fill=tk.BOTH)

def clear_all_data():
    if messagebox.askyesno("Confirmation", "Are you sure you want to clear all data?"):
        add_face.clear_faces_and_data()
        messagebox.showinfo("Info", "All faces and data have been cleared.")

def exit_application():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()

root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("400x300")

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TFrame", padding=20)

main_frame = ttk.Frame(root)
main_frame.pack(expand=True, fill=tk.BOTH)

ttk.Label(main_frame, text="Face Recognition Attendance System", font=("Helvetica", 16)).pack(pady=10)
ttk.Button(main_frame, text="Add New Face", command=add_face_gui).pack(pady=10)
ttk.Button(main_frame, text="Mark Attendance", command=mark_attendance_gui).pack(pady=10)
ttk.Button(main_frame, text="View Attendance", command=view_attendance).pack(pady=10)
ttk.Button(main_frame, text="Clear All Data", command=clear_all_data).pack(pady=10)
ttk.Button(main_frame, text="Exit", command=exit_application).pack(pady=10)

root.mainloop()
