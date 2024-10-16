import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Load the image using OpenCV
image_path = 'predicted_image3.png'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Find unique pixel values (these represent different segments)
unique_values = np.unique(image)

# Prepare to overlay text on the image
output_image = Image.fromarray(image).convert('RGB')  # Convert to RGB for text overlay
draw = ImageDraw.Draw(output_image)

# Optional: You can load a font for better visuals, otherwise default is used
# font = ImageFont.truetype("arial.ttf", 20)  # Path to font if available

# Loop over each unique segment (pixel value)
for value in unique_values:
    if value == 0:
        continue  # Skip background (assuming 0 is background)

    # Create a mask for this specific segment (all pixels with the same value)
    mask = np.where(image == value, 1, 0).astype(np.uint8)
    
    # Calculate moments to find the centroid
    M = cv2.moments(mask)
    
    if M["m00"] != 0:
        # Calculate centroid (center of mass)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # Draw the text at the centroid location
        draw.text((cX, cY), f'{value}', fill=(255, 0, 0))  # Red text

# Save the result
output_image.save('output_with_centroids.png')
output_image.show()

print("Centroids and text added to the image.")
