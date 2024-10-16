import os
import cv2
import numpy as np
from PIL import Image

# Define the original pixel values and their corresponding encoded labels
label_mapping = {
    0: 0,
    43: 1,
    54: 2,
    56: 3,
    73: 4,
    75: 5,
    76: 6,
    105: 7,
    143: 8,
    149: 9,
    178: 10,
    198: 11,
    225: 12
}

# Path to the folder containing the images
input_folder = 'version/training/combined masked/'

# Get all image file names in the folder
files = [f for f in os.listdir(input_folder) if f.endswith('.png')]

# Function to apply label encoding to each image
def label_encode_image(image, label_mapping):
    # Create a copy of the image to modify
    encoded_image = image.copy()

    # Loop over the label mapping and replace the original pixel values
    for original_value, encoded_value in label_mapping.items():
        encoded_image[image == original_value] = encoded_value

    return encoded_image

# Process each image
for file in files:
    file_path = os.path.join(input_folder, file)
    
    # Read the image in grayscale
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    
    # Apply label encoding
    encoded_image = label_encode_image(image, label_mapping)
    
    # Save the encoded image, replacing the original one
    Image.fromarray(encoded_image).save('version/training/combined masked/' + file)

print("Label encoding completed and images replaced.")
