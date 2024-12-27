import os
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
import threading
from rembg import remove
from PIL import Image
import numpy as np
import io

# Function to remove background and convert to grayscale
def process_image(input_path, output_path):
    # Open the image and remove the background
    with open(input_path, 'rb') as input_file:
        input_image = input_file.read()

    # Remove background
    output_image = remove(input_image)

    # Convert the result to a grayscale image (removes alpha channel)
    img = Image.open(io.BytesIO(output_image))
    img = img.convert('L')  # Convert to grayscale (mode 'L' for grayscale)

    # Save the processed image with the same name as input
    img.save(output_path)

# Function to process all images in the folder using threading
def process_images_in_parallel(source_folder, output_folder, index):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get all image files in the source folder (PNG or JPG)
    files = [f for f in os.listdir(source_folder) if f.endswith('.png') or f.endswith('.jpg')]
    files = files[index[0]: index[1]]
    print(f"Processing files: {files}")

    for file in files:
        # Construct paths (input and output paths will have the same name)
        input_path = os.path.join(source_folder, file)
        output_path = os.path.join(output_folder, file)

        # Process the image (remove background and convert to grayscale)
        process_image(input_path, output_path)

# Function to handle parallel processing of images
def parallel_process_images(source_folder, output_folder):
    # Get all files in the specified folder
    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    total_files = len(files)
    
    # Determine the chunk size for each thread
    chunk_size = total_files // 8
    remainder = total_files % 8

    threads = []
    start_index = 0

    # Create 8 threads for parallel processing
    for i in range(16):
        # Calculate end index for each chunk
        end_index = start_index + chunk_size + (1 if i < remainder else 0)

        # Create and start the thread
        thread = threading.Thread(target=process_images_in_parallel, args=(source_folder, output_folder, (start_index, end_index)))
        threads.append(thread)
        thread.start()

        # Update the start index for the next chunk
        start_index = end_index

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

# Example usage
source_folder = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.3/extra data/rgb'  # Path to the folder with images
output_folder = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.3/extra data/rgb2'  # Path to the folder to save processed images

# Start the parallel processing
parallel_process_images(source_folder, output_folder)
