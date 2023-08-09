import face_recognition as fr
import matplotlib.pyplot as plt
import shutil
import os

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

###-------------------------------MAIN------------------------------------###

#Make a face encoding of selected person
'''
while True:
    try:
        image_name = input("Type name of the selected image to look for the camper face: ")
    except:
        print("[ERROR:] Not a valid filename... please try again.")
'''
image_name = input("Type name of the selected image to look for the camper face: ")

print("___\n[PHASE1:] ENCODING & FACE RECOGNITION...\n---")##DEBUGGING
image_path = os.path.join(os.getcwd(), f"camper_list\{image_name}")
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
selected_face = int(input("Type the number of the face you want to choose: "))

face_encoding = face_encodings[selected_face]

# Search the album for similar faces
print("___\n[PHASE4:] SEARCH ALBUM FOR FACE...\n---")##DEBUGGING
album_dir = os.path.join(os.getcwd(), "Album")
export_dir = os.path.join(os.getcwd(), "Results")
found_photos = find_person_in_album(face_encoding,album_dir)

child_name = input("Type the name of child: ")

print("___\n[PHASE5:] MOVE FILES TO NEW DIRECTORY...\n---")##DEBUGGING
for filename in found_photos:
    source_path = os.path.join(album_dir, filename)
    destination_path = os.path.join(export_dir, child_name)

    try:
        shutil.move(source_path, destination_path)
    except:
        print(f"[ERROR:] failed to move {source_path} to {destination_path}")

print("[FINISHED...]")