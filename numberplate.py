from skimage.segmentation import clear_border
import pytesseract
import numpy as np
import imutils
import cv2
import easyocr
from matplotlib import pyplot as plt
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def imshow(title, image):

		# to show the image
    cv2.imshow(title, image)
        # check to see if we should wait for a keypress to exit image show
    cv2.waitKey(0)

def locate_probable_license_plates(gray, keep=5):

    # perform a blackhat morphological operation that will allow
    # us to reveal dark regions on light backgrounds
    # like the license plates. Because lecense plates are usually dark letters on light background
    rectKern = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKern)
    #debug_imshow("Blackhat", blackhat)
    
    squareKern = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    light = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, squareKern)
    light = cv2.threshold(light, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #debug_imshow("Light Regions", light)     
           
    gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F,dx=1, dy=0, ksize=-1)
    gradX = np.absolute(gradX)
    (minVal, maxVal) = (np.min(gradX), np.max(gradX))
    gradX = 255 * ((gradX - minVal) / (maxVal - minVal))
    gradX = gradX.astype("uint8")
    #debug_imshow("Scharr", gradX)

    gradX = cv2.GaussianBlur(gradX, (5, 5), 0)
    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKern)
    thresh = cv2.threshold(gradX, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #debug_imshow("Grad Thresh", thresh)

    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)
    #debug_imshow("Grad Erode/Dilate", thresh)

    thresh = cv2.bitwise_and(thresh, thresh, mask=light)
    thresh = cv2.dilate(thresh, None, iterations=2)
    thresh = cv2.erode(thresh, None, iterations=1)
    #debug_imshow("Final", thresh, waitKey=True)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:keep]
    # return the list of contours
    return cnts

def detect_the_license_plate(gray,candidates,clearBorder):
    # initialize the license plate contour and ROI
    lpCnt = None
    roi = None
    #print(candidates)
    probable_plates = []

    # loop over the license plate candidate contours
    for c in candidates:
        # compute the bounding box of the contour and then use
        # the bounding box to derive the aspect ratio
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        print(ar)

        #we will focus on the area if the ratio of rectangle is between 3 and 8

        if ar >= 3 and ar <= 8:
            # store the license plate contour and extract the
            # license plate from the grayscale image and then
            # threshold it
            lpCnt = c
            licensePlate = gray[y:y + h, x:x + w]
            roi = cv2.threshold(licensePlate, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            # check to see if we should clear any foreground
            # pixels touching the border of the image
            # (which typically, not but always, indicates noise)
            if clearBorder:
                roi = clear_border(roi)
            # display any debugging information and then break
            # from the loop early since we have found the license
            # plate region

            #debug_imshow("License Plate", licensePlate)
            #debug_imshow("ROI", roi)
            probable_plates.append([roi,lpCnt])
    # return a 2-tuple of the license plate ROI and the contour
    # associated with it
    return probable_plates   

def build_tesseract_options( psm=7):
    # tell Tesseract to only OCR alphanumeric characters
    alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    options = "-c tessedit_char_whitelist={}".format(alphanumeric)
    # set the PSM mode
    options += " --psm {}".format(psm)
    # return the built options string
    return options

def find_and_ocr(image, psm=7, clearBorder=True):
    # initialize the license plate text
    lpText = None
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # convert the input image to grayscale, locate all candidate
    # license plate regions in the image, and then process the
    # candidates, leaving us with the *actual* license plate
    candidates = locate_probable_license_plates(gray)
    plates = detect_the_license_plate(gray, candidates,clearBorder=clearBorder)
    # only OCR the license plate if the license plate ROI is not
    # empty
    #print("Returned plates ",plates)
    number_plates =[]
    for plate in plates:
        # OCR the license plate
        reader = easyocr.Reader(['en'])
        result = reader.readtext(plate[0])
        print('Esay OCR',result)
        options = build_tesseract_options(psm=psm)
        lpText = pytesseract.image_to_string(plate[0],config=options)
        print("Tesseract text",lpText)
        if result and result[0][-1]> 0.60:
            lpText = result[0][-2]
        if lpText and len(lpText)>7:
            number_plates.append([lpText,plate[1]])
    # return a 2-tuple of the OCR'd license plate text along with
    # the contour associated with the license plate region
    return number_plates

def cleanup_text(text):
	# strip out non-ASCII text so we can draw the text on the image
	# using OpenCV
	return "".join([c if ord(c) < 128 else "" for c in text]).strip()

