import tkinter as tk
from tkinter import filedialog

def openFile(path):
    path.set(filedialog.askopenfilename())

def openFolder(path):
    path.set(filedialog.askdirectory())

root = tk.Tk()
file_p = tk.StringVar()
button1 = tk.Button(text="Choose face",command=lambda: openFile(file_p))
button1.pack()

folder_p = tk.StringVar()
button2 = tk.Button(text="Select dataset",command=lambda: openFolder(folder_p))
button2.pack()

person_name = tk.StringVar()
text_box = tk.Entry(root, textvariable=person_name)
text_box.pack ()

def get_text(event):
    global file_p, folder_p
    person_name = text_box.get()
    print(f"FilePath: {file_p.get()}\n FolderPath: {folder_p.get()}\n Text: {person_name.get()}")
    root.destroy()

def check_loop():
    global file_p, folder_p, person_name
    if file_p.get() != "" and folder_p.get() != "" and person_name != "":
        text_box.bind('<Return>', get_text)
    else:
        root.after(100, check_loop)

root.after(100, check_loop)
root.mainloop()