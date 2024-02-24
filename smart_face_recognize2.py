# import datetime
# import cv2
# import numpy as np
# import numpy as npy12
# import face_recognition as face_rec
# import os
# import time
# from selenium_sms import send_message
# import res_numbers
#
#
# def resize(img, size):
#     if img is None or img.size == 0:
#         return None
#
#     width = int(img.shape[1] * size)
#     height = int(img.shape[0] * size)
#     dimension = (width, height)
#     return cv2.resize(img, dimension, interpolation=cv2.INTER_AREA)
#
#
# path = 'images'
# resident_img = []
# resident_name = []
# my_list = os.listdir(path)
#
#
# for jp in my_list:
#     img_path = f'{path}/{jp}'
#     curing = cv2.imread(img_path)
#     if curing is None:
#         print(f"Failed to load image: {img_path}")
#     else:
#         resident_img.append(curing)
#         resident_name.append(os.path.splitext(jp)[0])
# # for jp in my_list:
# #     curing = cv2.imread(f'{path}/{jp}')
# #     resident_img.append(curing)
# #     resident_name.append(os.path.splitext(jp)[0])
# def find_encoding(images):
#     img_encode = []
#     for img in images:
#         img = resize(img, 0.50)
#         if img is not None:
#             img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             encoding = face_rec.face_encodings(img)[0]
#             img_encode.append(encoding)
#     return img_encode
#
# last_attendance_time = {}
# def mark_attendance(name):
#     global last_attendance_time
#
#     # Get the current time
#     now = datetime.datetime.now()
#     time_str = now.strftime('%H:%M')
#
#     # If the person has not been marked before or if more than 5 seconds have passed
#     if name not in last_attendance_time or (now - last_attendance_time[name]).total_seconds() >= 43200:
#         with open('attendance.csv', 'a') as f:
#             f.write(f"{name},{time_str}\n")
#         send_message(name=name,number=res_numbers.resident_numbers[name])
#
#         # Update the last attendance time for the person
#         last_attendance_time[name] = now
#
# encode_list = find_encoding(resident_img)
#
# vid = cv2.VideoCapture(0)
#
# while True:
#     success,frame = vid.read()
#     smaller_frame = cv2.resize(frame,(0,0),None,0.25,0.25)
#     faces_in_frame = face_rec.face_locations(smaller_frame)
#     encode_faces_in_frame = face_rec.face_encodings(smaller_frame,faces_in_frame)
#
#     for encode_face, face_location in zip(encode_faces_in_frame,faces_in_frame):
#         matches = face_rec.compare_faces(encode_list, encode_face)
#         facedis = face_rec.face_distance(encode_list,encode_face)
#         print(facedis)
#         match_index = np.argmin(facedis)
#
#         if matches[match_index]:
#             name = resident_name[match_index].upper()
#             y1,x2,y2,x1 = face_location
#             y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
#             cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),3)
#             cv2.rectangle(frame,(x1,y2-25),(x2,y2),(0,255,0),cv2.FILLED)
#             cv2.putText(frame, name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
#
#             mark_attendance(name)
#
#         cv2.imshow('video',frame)
#         cv2.waitKey(1)
#
#
import datetime
import cv2
import numpy as np
import face_recognition as face_rec
import os
import tkinter as tk
from tkinter import messagebox
from selenium_sms import send_message
import res_numbers
from PIL import Image, ImageTk

def resize(img, size):
    if img is None or img.size == 0:
        return None

    width = int(img.shape[1] * size)
    height = int(img.shape[0] * size)
    dimension = (width, height)
    return cv2.resize(img, dimension, interpolation=cv2.INTER_AREA)


def load_resident_images(path):
    resident_img = []
    resident_name = []
    my_list = os.listdir(path)

    for jp in my_list:
        img_path = f'{path}/{jp}'
        curing = cv2.imread(img_path)
        if curing is not None:
            resident_img.append(curing)
            resident_name.append(os.path.splitext(jp)[0])
        else:
            print(f"Failed to load image: {img_path}")

    return resident_img, resident_name


def find_encoding(images):
    img_encode = []
    for img in images:
        img = resize(img, 0.50)
        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encoding = face_rec.face_encodings(img)[0]
            img_encode.append(encoding)
    return img_encode


def mark_attendance(name):
    global last_attendance_time

    # Get the current time
    now = datetime.datetime.now()
    time_str = now.strftime('%H:%M')

    # If the person has not been marked before or if more than 5 seconds have passed
    if name not in last_attendance_time or (now - last_attendance_time[name]).total_seconds() >= 43200:
        with open('attendance.csv', 'a') as f:
            f.write(f"{name},{time_str}\n")
        send_message(name=name, number=res_numbers.resident_numbers[name])

        # Update the last attendance time for the person
        last_attendance_time[name] = now

def on_exit(root):
    vid.release()
    cv2.destroyAllWindows()
    root.destroy()


def main():
    global vid, last_attendance_time

    path = 'images'
    resident_img, resident_name = load_resident_images(path)
    encode_list = find_encoding(resident_img)

    vid = cv2.VideoCapture(0)

    root = tk.Tk()
    root.title("Face Recognition App")

    canvas = tk.Canvas(root, width=640, height=480)
    canvas.pack()

    def process_frame():
        success, frame = vid.read()
        if not success:
            print("Failed to get frame from the video stream.")
            return

        smaller_frame = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        faces_in_frame = face_rec.face_locations(smaller_frame)
        encode_faces_in_frame = face_rec.face_encodings(smaller_frame, faces_in_frame)

        for encode_face, face_location in zip(encode_faces_in_frame, faces_in_frame):
            matches = face_rec.compare_faces(encode_list, encode_face)
            facedis = face_rec.face_distance(encode_list, encode_face)
            print(facedis)
            match_index = np.argmin(facedis)

            if matches[match_index]:
                name = resident_name[match_index].upper()
                y1, x2, y2, x1 = face_location
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv2.rectangle(frame, (x1, y2 - 25), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

                mark_attendance(name)

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (640, 480))
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        canvas.imgtk = imgtk
        canvas.create_image(0, 0, anchor="nw", image=imgtk)
        root.after(10, process_frame)
    process_frame()
    root.protocol("WM_DELETE_WINDOW", lambda: on_exit(root))
    root.mainloop()


if __name__ == "__main__":
    last_attendance_time = {}
    main()
