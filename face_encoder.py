import face_recognition as fr
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog

##------------------------FUNCTIONS------------------------------###
def find_person_in_album(known_encoding, album_folder):
    found_images = []

    for filename in os.listdir(album_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(album_folder, filename)
            unknown_image = fr.load_image_file(image_path)
            unknown_face_encodings = fr.face_encodings(unknown_image)

            for unknown_encoding in unknown_face_encodings:
                result = fr.compare_faces([known_encoding], unknown_encoding)
                if result[0]:
                    found_images.append(image_path)
                    break
    return found_images

def openFile(path):
    path.set(filedialog.askopenfilename())

def openFolder(path):
    path.set(filedialog.askdirectory())

def get_text(event):
    global file_p, folder_p, export_p
    person_name = text_box.get()
    root.destroy()

def check_loop():
    global file_p, folder_p, person_name
    if file_p.get() != "" and folder_p.get() != "" and export_p.get() != "" and person_name.get() != "":
        text_box.bind('<Return>', get_text)
    else:
        root.after(100, check_loop)

###-------------------------------MAIN------------------------------------###

# start the GUI for file selection

root = tk.Tk()
file_p = tk.StringVar()
button1 = tk.Button(text="Choose face",command=lambda: openFile(file_p))
button1.pack()

folder_p = tk.StringVar()
button2 = tk.Button(text="Select dataset",command=lambda: openFolder(folder_p))
button2.pack()

export_p = tk.StringVar()
button3 = tk.Button(text="Select export path",command=lambda: openFolder(export_p))
button3.pack()

person_name = tk.StringVar()
text_box = tk.Entry(root, textvariable=person_name)
text_box.pack ()

root.after(100, check_loop)
root.mainloop()

##-------------------RUN THE PROCESS-----------------------##
print("___\n[PHASE0:] FOLDER & FILE SELECTION...\n---")##DEBUGGING
print(f"FilePath: {file_p.get()}\nFolderPath: {folder_p.get()}\nExportPath: {export_p.get()}\nName: {person_name.get()}")

print("___\n[PHASE1:] ENCODING & FACE RECOGNITION...\n---")##DEBUGGING
image_path = os.path.normpath(file_p.get())
image = fr.load_image_file(image_path)
face_locations = fr.face_locations(image)
face_encodings = fr.face_encodings(image, face_locations)

print("___\n[PHASE2:] SHOW FACES...\n---")##DEBUGGING
count = 0
fig, ax = plt.subplots()
for face_location in face_locations:
    top,right,bottom,left = face_location
    rect = plt.Rectangle((left, top), right - left, bottom - top, fill=False, edgecolor=(0, 0, 1), linewidth=2)
    ax.add_patch(rect)
    ax.text(left, top - 10, str(count), color='red', fontsize=12, backgroundcolor=(0, 0, 0, 0.6))
    count += 1

plt.imshow(image)
plt.axis('off')
plt.show()

print("___\n[PHASE3:] SELECT FACE...\n---")##DEBUGGING
if len(face_locations) == 1:
    selected_face = 0
    print("only one face found... choosing this face...")
else:
    selected_face = input("Type the number of the face you want to choose: ")

face_encoding = face_encodings[int(selected_face)]

# Search the album for similar faces
print("___\n[PHASE4:] SEARCH ALBUM FOR FACE...\n---")##DEBUGGING

album_dir = os.path.normpath(folder_p.get())
export_dir = os.path.join(os.path.normpath(export_p.get()), person_name.get())

found_photos = find_person_in_album(face_encoding,album_dir)

print("___\n[PHASE5:] MOVE FILES TO NEW DIRECTORY...\n---")##DEBUGGING
for filename in found_photos:
    source_path = os.path.join(album_dir, filename)

    try:
        destination_path = os.path.join(export_dir, filename)
        os.rename(source_path, destination_path)
    except:
        print(f"[ERROR:] failed to move {source_path} to {export_dir}")

print("[FINISHED...]")
