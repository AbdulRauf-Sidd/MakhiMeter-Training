import os
import cv2
import numpy as np
from PIL import Image
import concurrent.futures
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Function to apply label encoding to each image
def label_encode_image(file_path, label_mapping):
    # Read the image in grayscale
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    # Create a copy of the image to modify
    encoded_image = image.copy()

    # Loop over the label mapping and replace the original pixel values
    for original_value, encoded_value in label_mapping.items():
        encoded_image[image == original_value] = encoded_value

    # Save the encoded image, replacing the original one
    output_path = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.2/experiment_2/background_removed/labeled encoded/' + os.path.basename(file_path)
    Image.fromarray(encoded_image).save(output_path)
    
# Function to process images in parallel
def process_images_in_parallel(files, input_folder, label_mapping):
    # Prepare the full file paths for each image
    file_paths = [os.path.join(input_folder, f) for f in files]

    # Use ThreadPoolExecutor to process images in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit each image encoding task to the executor
        futures = [executor.submit(label_encode_image, file_path, label_mapping) for file_path in file_paths]

        # Wait for all futures to complete
        concurrent.futures.wait(futures)

# Example usage

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

input_folder = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.2/experiment_2/background_removed/augmented masked/'
files = [f for f in os.listdir(input_folder) if f.endswith('.png')]
process_images_in_parallel(files, input_folder, label_mapping)
print("Label encoding completed and images replaced.")
