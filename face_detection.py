import cv2
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
import os

def detect_faces(image,path):

       
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces_image = []
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    count = 1
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        list = []
        list.append(x)
        list.append(y)
        list.append(w)
        list.append(h)
        faces_image.append(list)
        crop_img = image[y:y+h, x:x+w]
        
        cv2.imwrite(os.path.join(path , 'person'+str(count)+'.jpg'), crop_img)

    return faces_image