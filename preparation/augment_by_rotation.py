from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os
from PIL import Image

def augment_images_with_rotation(source_folder_rgb, source_folder_mask, output_folder_rgb, output_folder_mask):
    # Ensure output folders exist
    os.makedirs(output_folder_rgb, exist_ok=True)
    os.makedirs(output_folder_mask, exist_ok=True)

    # Get all file names from the RGB folder assuming both folders contain the same names
    files = [f for f in os.listdir(source_folder_rgb) if f.endswith('.png')]
    print(files)
    
    for file in files:
        # Construct paths
        file_path_rgb = os.path.join(source_folder_rgb, file)
        file_path_mask = os.path.join(source_folder_mask, file)
        
        # Load images without resizing or converting to grayscale
        img_rgb = Image.open(file_path_rgb)
        img_mask = Image.open(file_path_mask)
        
        # Convert images to arrays
        img_rgb = np.array(img_rgb)
        img_mask = np.array(img_mask)
        
        # Define rotation angles
        angles = [90, 180, 270]
        
        for angle in angles:
            # Rotate RGB and mask images by the specified angle
            rotated_rgb = np.rot90(img_rgb, k=angle // 90)  # Rotate by 90, 180, or 270 degrees
            rotated_mask = np.rot90(img_mask, k=angle // 90)
            
            # Convert rotated arrays back to images
            rotated_rgb_image = Image.fromarray(rotated_rgb)
            rotated_mask_image = Image.fromarray(rotated_mask)
            
            # Save rotated images with consistent naming
            rotated_rgb_image.save(os.path.join(output_folder_rgb, f'rot_{angle}_{file}'))
            rotated_mask_image.save(os.path.join(output_folder_mask, f'rot_{angle}_{file}'))

# Define paths
source_folder_rgb = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model v1.2/experiment/combined rgb'
source_folder_mask = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model v1.2/experiment/combined masked'
output_folder_rgb = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model v1.2/experiment/rotated_rgb'
output_folder_mask = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model v1.2/experiment/rotated_masked'

# Run the function
augment_images_with_rotation(source_folder_rgb, source_folder_mask, output_folder_rgb, output_folder_mask)
