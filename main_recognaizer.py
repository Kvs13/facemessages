# packages dlib , cmake, opencv, numpi ,numpy
import face_recognition as face_rec
import cv2
import numpy as npy

#обработка картинок
def resize(img,size):
    width = int(img.shape[1]*size)
    height = int(img.shape[0]*size)
    dimension = (width,height)
    return cv2.resize(img,dimension,interpolation=cv2.INTER_AREA)


person1 = face_rec.load_image_file('images/Serdar.jpg')
person1 = cv2.cvtColor(person1,cv2.COLOR_BGR2RGB)
person1 = resize(person1,0.50)

#поиск лица
face_location_person1 = face_rec.face_locations(person1)[0]
encoed_person1 = face_rec.face_encodings(person1)[0]
cv2.rectangle(person1,(face_location_person1[3],face_location_person1[0]),(face_location_person1[1],face_location_person1[2]),(0,255,255),3)

# res = face_rec.compare_faces([encoed_person1],encoed_person2) #для сравнивания с другими фото

cv2.imshow('main_img',person1)
cv2.waitKey(0)
cv2.destroyAllWindows()