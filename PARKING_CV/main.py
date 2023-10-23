import cv2
from slots import viewAvailable 

tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
images = ["PARKINGLOT2-1.png", "PARKINGLOT2-2.png", "PARKINGLOT2-3.png", "PARKINGLOT2-4.png", "PARKINGLOT2-5.png", "PARKINGLOT2-6.png", "PARKINGLOT2-8.png", "PARKINGLOT2-9.png", "PARKINGLOT2-10.png",]

for im in images:
    img = viewAvailable(im, tesseract_path)
    cv2.imshow("Image", img)
    print(im)
    cv2.waitKey(0)
