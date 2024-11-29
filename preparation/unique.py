import os
import cv2
import numpy as np

def collect_unique_pixel_values(folder_path):
    # Set to store unique pixel values from all images
    unique_pixel_values = set()
    
    # Get all image file names in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]

    for file in files:
        # Construct the full file path
        file_path = os.path.join(folder_path, file)
    
    # Read the image using OpenCV and convert it to grayscale
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    
    # Get unique pixel values and update the set
        unique_values = np.unique(image)
        unique_pixel_values.update(unique_values)
    
    # Print the combined set of unique pixel values
    print(f"Unique pixel values across all images: {unique_pixel_values}")

# Specify the folder path containing the images
folder_path = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.2/experiment_2/with_rotation/size 256/interpolated/labeled encoded/'

# Call the function
collect_unique_pixel_values(folder_path)
