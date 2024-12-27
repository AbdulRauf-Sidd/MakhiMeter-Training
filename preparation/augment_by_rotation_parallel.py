from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os
from PIL import Image
import threading

def augment_images_with_rotation(source_folder_rgb, source_folder_mask, output_folder_rgb, output_folder_mask, index):
    # Ensure output folders exist
    os.makedirs(output_folder_rgb, exist_ok=True)
    os.makedirs(output_folder_mask, exist_ok=True)

    # Get all file names from the RGB folder assuming both folders contain the same names
    files = [f for f in os.listdir(source_folder_rgb) if f.endswith('.png') or f.endswith('.jpg')]
    files = files[index[0]: index[1]]
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


def parallel_process_files(source_rgb, source_masked, output_rgb, output_masked):
    # Get all files in the specified folder
    files = [f for f in os.listdir(source_rgb) if os.path.isfile(os.path.join(source_rgb, f))]
    total_files = len(files)
    
    # Determine the chunk size for each thread
    chunk_size = total_files // 8
    remainder = total_files % 8

    threads = []
    start_index = 0

    # Create 8 threads
    for i in range(16):
        # Calculate end index for each chunk
        end_index = start_index + chunk_size + (1 if i < remainder else 0)

        
        # Create a thread with the target function and 5 parameters
        thread = threading.Thread(target=augment_images_with_rotation, args=(source_rgb, source_masked, output_rgb, output_masked, (start_index, end_index)))
        threads.append(thread)
        
        # Start the thread
        thread.start()
        
        # Update start index for the next chunk
        start_index = end_index

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

# Define paths
source_folder_rgb = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.3/extra data/rgb2/'
source_folder_mask = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.3/extra data/masked/'
output_folder_rgb = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.3/extra data/rgb2 aug'
output_folder_mask = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.3/extra data/masked aug'
# Run the function
parallel_process_files(source_folder_rgb, source_folder_mask, output_folder_rgb, output_folder_mask)
