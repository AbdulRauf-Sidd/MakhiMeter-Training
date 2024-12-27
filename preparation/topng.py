import os
from PIL import Image, ImageOps
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def convert_images_to_png(source_dir, output_dir):
    # Check if output directory exists, create if not
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Iterate over all files in the source directory
    for filename in os.listdir(source_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.tif', '.bmp', '.gif', '.tiff')):  # Add any other file formats you expect
            file_path = os.path.join(source_dir, filename)
            # Open the image file
            with Image.open(file_path) as img:
                # Apply EXIF orientation (fix rotation if needed)
                img = ImageOps.exif_transpose(img)
                
                # Remove extension and add .png
                new_filename = os.path.splitext(filename)[0] + '.png'
                output_path = os.path.join(output_dir, new_filename)
                
                # Convert and save image as PNG
                img.save(output_path, 'PNG')


source_dir = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.3/extra data/rgb'
output_dir = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.3/extra data/rgb'
convert_images_to_png(source_dir, output_dir)
