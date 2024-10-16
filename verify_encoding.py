import os
import cv2
import numpy as np

# Path to the folder containing the images
input_folder = 'version/training/combined masked/'

# Get all image file names in the folder
files = [f for f in os.listdir(input_folder) if f.endswith('.png')]

# Initialize a set to store unique pixel values (set ensures uniqueness)
unique_pixel_values = set()

# Process each image
for file in files:
    file_path = os.path.join(input_folder, file)
    
    # Read the image in grayscale
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    
    # Get unique values in this image and add them to the set
    unique_values_in_image = np.unique(image)
    unique_pixel_values.update(unique_values_in_image)

# Convert the set to a sorted list
unique_pixel_values = sorted(list(unique_pixel_values))

# Print the list of unique pixel values
print(f"Unique pixel values in all images: {unique_pixel_values}")
