import os
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def collect_unique_pixel_values_from_image(file_path):
    # Read the image using OpenCV and convert it to grayscale
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    
    # Get unique pixel values from the image
    unique_values = np.unique(image)
    
    return unique_values

def collect_unique_pixel_values(folder_path):
    # Set to store unique pixel values from all images
    unique_pixel_values = set()
    
    # Get all image file names in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]

    # List to store file paths
    file_paths = [os.path.join(folder_path, file) for file in files]

    # Using ThreadPoolExecutor to process images in parallel
    with ThreadPoolExecutor() as executor:
        # Map the function to the files in parallel
        results = executor.map(collect_unique_pixel_values_from_image, file_paths)

        # Combine all the results (unique values from each image) into the final set
        for result in results:
            unique_pixel_values.update(result)
    
    # Print the combined set of unique pixel values
    print(f"Unique pixel values across all images: {sorted(unique_pixel_values)}")

# Specify the folder path containing the images
folder_path = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.2/experiment_2/with_rotation/size 256/interpolated/labeled encoded/'

# Call the function
collect_unique_pixel_values(folder_path)
