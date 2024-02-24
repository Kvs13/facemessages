import cv2
import numpy as npy
import face_recognition as face_rec
import os



def resize(img,size):
    width = int(img.shape[1]*size)
    height = int(img.shape[0]*size)
    dimension = (width,height)
    return cv2.resize(img,dimension,interpolation=cv2.INTER_AREA)

path = 'images'
persons_img = []
person_names = []
my_list = os.listdir(path)
# print(my_list)
for prsn in my_list:
    cur_img = cv2.imread(f'{path}/{prsn}')
    persons_img.append(cur_img)
    person_names.append(os.path.splitext(prsn)[0])

def findEncode(images):
    en_list = []
    for img in images:
        # img = resize(img,0.50) #resize foto
        # img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)# skin color change
        encode_img = face_rec.face_encodings(img)[0]
        en_list.append(encode_img)
    return en_list

en_list = findEncode(persons_img)

vid = cv2.VideoCapture(0)

while True:
    success,frame = vid.read()
    frames = cv2.resize(frame,(0,0),None,0.25,0.25)
    frames = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)

    faces_in_frame = face_rec.face_locations(frames)
    encode_in_frame = face_rec.face_encodings(frames, faces_in_frame)






