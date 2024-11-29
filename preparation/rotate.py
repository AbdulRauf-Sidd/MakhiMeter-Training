import cv2
import numpy as np
from PIL import Image

# Load the image in grayscale
image = cv2.imread('/home/abdulrauf/Projects/MakhiMeter-Training/testing_256.png', cv2.IMREAD_GRAYSCALE)

# Resize the image to 128x128
target_size = (256, 256)
resized_image = cv2.resize(image, target_size, interpolation=cv2.INTER_NEAREST)

# Rotate the image by 10 degrees
height, width = resized_image.shape
center = (width // 2, height // 2)

# Define the rotation matrix
rotation_matrix = cv2.getRotationMatrix2D(center, 15, 1)  # 10 degrees, no scaling

# Apply the rotation using warpAffine
rotated_image = cv2.warpAffine(resized_image, rotation_matrix, (width, height), flags=cv2.INTER_NEAREST)

# Save the rotated image
Image.fromarray(rotated_image).save('/home/abdulrauf/Projects/MakhiMeter-Training/testing_256_rotated.png')
