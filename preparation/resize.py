# Path to the folder containing the images
input_folder = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/combined masked 7/'

import os
import cv2
from PIL import Image

# Set the target size for resizing
target_size = (256, 256)

# Get all image file names in the folder
files = [f for f in os.listdir(input_folder) if f.endswith('.png')]

# Ensure the output folder exists
output_folder = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/combined masked 7/'
os.makedirs(output_folder, exist_ok=True)

# Process each image
for file in files:
    file_path = os.path.join(input_folder, file)
    
    # Read the image in grayscale
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    
    # Resize the image to 128x128
    resized_image = cv2.resize(image, target_size, interpolation=cv2.INTER_NEAREST)
    
    # Save the resized image
    output_path = os.path.join(output_folder, file)
    Image.fromarray(resized_image).save(output_path)

print("Images successfully resized to 256x256 and saved.")
