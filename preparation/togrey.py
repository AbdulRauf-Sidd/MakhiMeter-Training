# Path to the folder containing the images
input_folder = '/home/abdulrauf/Projects/makhi_meter_dataset/version/training/combined rgb/'


import os
import cv2
import numpy as np
from PIL import Image


# Get all image file names in the folder
files = [f for f in os.listdir(input_folder) if f.endswith('.png')]


# Process each image
for file in files:
    file_path = os.path.join(input_folder, file)
    
    # Read the image in grayscale
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    
    
    
    # Apply label encoding
    
    
    # Save the encoded image, replacing the original one
    Image.fromarray(image).save('version/training/combined rgb/' + file)

print("greyed.")
