from PIL import Image
import os
import concurrent.futures
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def process_image(file_path, hex_colors, grey, output_dir):
    # Convert the list of hex colors to a list of RGB tuples
    allowed_colors = [tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) for hex_color in hex_colors]
    
    image = Image.open(file_path)
    if grey:
        image = image.convert("L")
    
    pixels = image.load()

    # Process each pixel
    for i in range(image.width):
        for j in range(image.height):
            if pixels[i, j][:3] not in allowed_colors:  # Check if the pixel color is not allowed
                pixels[i, j] = (0, 0, 0)  # Set non-matching pixels to black

    # Save the modified image
    filename = os.path.basename(file_path)
    output_path = os.path.join(output_dir, filename)
    image.save(output_path)

def process_images(directory, hex_colors, grey, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get a list of all image files in the directory
    image_files = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith(".png")]

    # Use ThreadPoolExecutor to process images in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit each image processing task to the executor
        futures = [
            executor.submit(process_image, file_path, hex_colors, grey, output_dir)
            for file_path in image_files
        ]
        
        # Wait for all futures to complete
        concurrent.futures.wait(futures)

# Example usage
directory_path = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model v1.4/original masked'
output_dir = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model v1.4/original masked'
hex_colors = ['00ff00', 'ff0000', '0000ff', '1d19b5', 'ffff00', 'ff00ff', '00ffff', '691369']  # Example hex colors

process_images(directory_path, hex_colors, grey=False, output_dir=output_dir)
