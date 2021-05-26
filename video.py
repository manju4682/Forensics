import cv2
import time
import imutils
import numberplate
import face_detection
from datetime import datetime
import os
camera = cv2.VideoCapture(0)

def Listener():  
    
    while True:    
        input(">")
        print("Alarm was triggered!")
        return_value, image = camera.read()
        conti = evidence_collector(image)
        if conti:
            continue
        else:
            break    

def evidence_collector(image):
    
    now = datetime.now()
    time_now = now.strftime("%m_%d_%Y__%H_%M_%S")
    directory = time_now
    parent_directory = r'C:\Users\Manjunath\Desktop\Python files\Forensics\Evidence'
    path = os.path.join(parent_directory, directory)
    os.mkdir(path)
    
    image = imutils.resize(image, width=600)
    
    faces = face_detection.detect_faces(image,path)
    number_plates = numberplate.find_and_ocr(image)
    no_of_faces = 0
    no_of_cars_detected = 0
    for face in faces:
        no_of_faces +=1
        cv2.rectangle(image, (face[0], face[1]), (face[0]+face[2], face[1]+face[3]), (0, 255, 0), 2)

    for plate in number_plates:
        # fit a rotated bounding box to the license plate contour and
        # draw the bounding box on the license plate
        no_of_cars_detected +=1
        box = cv2.boxPoints(cv2.minAreaRect(plate[1]))
        box = box.astype("int")
        cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
        # compute a normal (unrotated) bounding box for the license
        # plate and then draw the OCR'd license plate text on the
        # image
        (x, y, w, h) = cv2.boundingRect(plate[1])
        cv2.putText(image, numberplate.cleanup_text(plate[0]), (x-5, y - 15),
            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)    
    
    print(no_of_faces," ",no_of_cars_detected)

    cv2.imwrite(os.path.join(path ,'complete.jpg'), image)
    return True
    

if __name__ == "__main__":
    Listener()


