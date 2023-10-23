# import the necessary packages
import numpy as np
import imutils
import cv2
from ocr import numAvailable

def viewAvailable(imgFile, tessPath):



    # load the image, convert it to grayscale, and blur it slightly
    image = cv2.imread(imgFile)

    gray = cv2.cvtColor(20 + image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, None, h=80, templateWindowSize=4, searchWindowSize=20)

    # edge detection, dilation + erosion to close gaps in between object edges
    edged = cv2.Canny(denoised, 30, 50)
    edged = cv2.dilate(edged, None, iterations=2)
    edged = cv2.erode(edged, None, iterations=1)
    cv2.imshow("Image", edged)

    # find contours in the edge map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    numCars = 0
    for c in cnts:
        # compute the rotated bounding box of the contour
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")

        # if the contour is not sufficiently large or very large, ignore it
        if cv2.contourArea(c) < 1100 or cv2.contourArea(c) > 25000:
            continue
        # if it is smaller than an average car
        elif cv2.contourArea(c) > 1100 and cv2.contourArea(c) < 2000:
            # Calculate the center of the bounding box
            center_x = int(np.mean(box[:, 0]))
            center_y = int(np.mean(box[:, 1]))
            # enlarge green box
            for i in range(4):
                box[i][0] = center_x + (box[i][0] - center_x) * (1.4)
                box[i][1] = center_y + (box[i][1] - center_y) * (2.4)
            # green lines
            cv2.drawContours(image, [box.astype("int")], -1, (100, 255, 100), 2)
        else:
            numCars += 1
            # red lines
            cv2.drawContours(image, [box.astype("int")], -1, (0, 0, 255), 3)

    # draw the object sizes on the image
    cv2.putText(image, "Cars: "+ str(numCars), (30, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)

    n = numAvailable(imgFile, tessPath)
    cv2.putText(image, "Available: "+ str(n), (30, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
    #show the output image
    return image