from PIL import Image
import numpy as np
import os

def load_image_as_rgb(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        filename = os.path.basename(image_path)
        # Convert image to RGB if not already
        if img.mode != 'RGB':
            img = img.convert('RGB')
        # Convert image to numpy array
        img_array = np.array(img)
        Image.fromarray(img_array).save('version/test/' + filename)
    return img_array

# Example usage:
source_folder = '/home/abdulrauf/Projects/makhi_meter_dataset/version/training/perfect binary'
files = os.listdir(source_folder)

# Process each file
for file in files:
    file_path = os.path.join(source_folder, file)
    img_array = load_image_as_rgb(file_path)
    print(file, img_array.shape)  # This will print (512, 512, 3) for all images
