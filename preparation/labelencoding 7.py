import os
import cv2
import numpy as np
from PIL import Image

# Define the original pixel values and their corresponding encoded labels
label_mapping = {
    0: 0,
    43: 1,
    54: 2,
    76: 3,
    105: 4,
    149: 5,
    178: 6,
    225: 7,
}

# Path to the folder containing the images
input_folder = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/combined masked 7/7/'

# Get all image file names in the folder
files = [f for f in os.listdir(input_folder) if f.endswith('.png')]

# Function to apply label encoding to each image
def label_encode_image(image, label_mapping):
    # unique_pixel_values = set()
    # image_array = np.array(image)
        
    #     # Get unique pixel values and update the set
    # unique_values = np.unique(image_array)
    # unique_pixel_values.update(unique_values)
    # print(unique_pixel_values)
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
    Image.fromarray(encoded_image).save('/home/abdulrauf/Projects/MakhiMeter-Training/data/training/combined masked 7/7/' + file)

print("Label encoding completed and images replaced.")
