from PIL import Image, ImageEnhance
import pytesseract
import cv2
import os
import matplotlib.pyplot as plt
from scipy import ndimage
import numpy as np


def numAvailable(image_path, tpath):
    pytesseract.pytesseract.tesseract_cmd = tpath

    # Ensure the image file exists
    if not os.path.isfile(image_path):
        print("The specified image file does not exist.")
    else:
        # Load the image and convert it to grayscale
        image = cv2.imread(image_path)
        image = ndimage.median_filter(image, 2)
        image = ndimage.gaussian_filter(image,4)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = 255 - gray

        # Threshold the grayscale image to create a binary image
        _, gray = cv2.threshold(gray, 55, 255, cv2.THRESH_BINARY | cv2.THRESH_BINARY)
        #Perform OCR on the thresholded image to extract white text
        text = pytesseract.image_to_string(Image.fromarray(gray))

        count = 0 
        for i in text:
            if i == 'p' or i == 'P':
                count+=1

        return count
    
        '''
        # Print the OCR result
        print("OCR Result:\n")
        print(text,"\n")
        print(count)
        # Display the thresholded image using Matplotlib
        plt.imshow(gray, cmap='gray')
        plt.title(image_path.strip('".png'))
        plt.axis('off')  # Turn off axis labels
        plt.show()'''