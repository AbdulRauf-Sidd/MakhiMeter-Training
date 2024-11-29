
import os
import cv2
from PIL import Image

# Set the target size for resizing
input_folder = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/normalized/'
target_size = (256, 256)

# Get all image file names in the folder
files = [f for f in os.listdir(input_folder) if f.endswith('.png')]

# Ensure the output folder exists
output_folder = 'data/training/normalized binary/'
os.makedirs(output_folder, exist_ok=True)

# Process each image
for file in files:
    file_path = os.path.join(input_folder, file)
    
    # Read the image in grayscale
    # image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    gray_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    # gray_image = cv2.equalizeHist(gray_image)
    # Step 2: Convert to binary image u.convert('L').resize((256, 256))sing thresholding
    _, binary_image = cv2.threshold(gray_image, 45, 255, cv2.THRESH_BINARY)
    inverted_image = cv2.bitwise_not(binary_image)
    # Step 3: Apply dilation and erosion
    # Define the kernel size
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # Dilation
    # dilated_image = cv2.dilate(inverted_image, kernel, iterations=1)
    # eroded_image = cv2.erode(dilated_image, kernel, iterations=0)
    # Resize the image to 128x128
    # resized_image = cv2.resize(image, target_size, interpolation=cv2.INTER_NEAREST)
    
    # Save the resized image
    output_path = os.path.join(output_folder, file)
    Image.fromarray(inverted_image).save(output_path)

print("Images successfully Converted to binary.")