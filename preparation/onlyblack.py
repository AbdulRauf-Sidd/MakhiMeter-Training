from PIL import Image
import os

def process_images(directory, hex_colors):
    # Convert the list of hex colors to a list of RGB tuples
    allowed_colors = [tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) for hex_color in hex_colors]
    count = 0
    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".png"):  # Check if the file is an image, adjust as needed for other formats
            file_path = os.path.join(directory, filename)
            image = Image.open(file_path)
            pixels = image.load()
            

            # Process each pixel
            for i in range(image.width):
                for j in range(image.height):
                    if pixels[i, j][:3] not in allowed_colors:  # Check if the pixel color is not allowed
                        pixels[i, j] = (0, 0, 0)  # Set non-matching pixels to black

            # Save the modified image
            image.save('version/training/defected masked (256)/{0}'.format(filename))  # Overwrite the original image
            # Or save as a new file:
            # image.save(os.path.join(directory, f"modified_{filename}"))

# Example usage
directory_path = 'version/training/defected masked (256)'
hex_colors = ['00ff00', 'ff0000', '0000ff', '1d19b5', 'ffff00', 'ff00ff', '00ffff',
              '691369', '1f6d11', 'a6d3d9', '4e3610', '1d5d5b', 'df6d6d']  # Example hex colors
process_images(directory_path, hex_colors)
