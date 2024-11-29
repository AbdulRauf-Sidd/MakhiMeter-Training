import os
import numpy as np
from PIL import Image

def rotate_single_image(image_path, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Open the RGB image
    img_rgb = Image.open(image_path)
    
    # Convert image to an array
    img_rgb = np.array(img_rgb)
    
    # Define rotation angles
    angles = [90, 180, 270]
    
    # Get the base name of the image file
    file_name = os.path.basename(image_path)
    base_name = os.path.splitext(file_name)[0]
    
    for angle in angles:
        # Rotate the RGB image by the specified angle
        rotated_rgb = np.rot90(img_rgb, k=angle // 90)  # Rotate counter-clockwise
        
        # Convert the rotated array back to an image
        rotated_rgb_image = Image.fromarray(rotated_rgb)
        
        # Save the rotated image with a consistent name
        rotated_filename = f'{base_name}_rot_{angle}.png'
        rotated_rgb_image.save(os.path.join(output_folder, rotated_filename))
        print(f"Saved rotated image: {rotated_filename}")

# Example usage
image_path = 'data/training/model_v1.2/experiment/abc/D.bizonata_f_02.png'  # Replace with the path to your RGB image
output_folder = 'data/training/model_v1.2/experiment/abc'  # Replace with your desired output folder

rotate_single_image(image_path, output_folder)
