from PIL import Image
import os

def process_images(directory, hex_colors, grey):
    # Convert the list of hex colors to a list of RGB tuples
    allowed_colors = [tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) for hex_color in hex_colors]
    count = 0
    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".png"):  # Check if the file is an image, adjust as needed for other formats
            print("hi")
            file_path = os.path.join(directory, filename)
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
            image.save('/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.2/experiment_2/with_rotation/size 256/interpolated/augmented masked/{0}'.format(filename))  # Overwrite the original image
            # Or save as a new file:
            # image.save(os.path.join(directory, f"modified_{filename}"))

# Example usage
directory_path = '/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.2/experiment_2/with_rotation/size 256/interpolated/augmented masked'
hex_colors = ['00ff00', 'ff0000', '0000ff', '1d19b5', 'ffff00', 'ff00ff', '00ffff',
              '691369']  # Example hex colors

grey_hex_colors = ['959595', '4c4c4c', 'b2b2b2', '2b2b2b', '363636', '696969', 'e1e1e1',
              'c6c6c6']  # Example hex colors
process_images(directory_path, hex_colors, grey=False)


# image = Image.open('/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.2/experiment/abc/D.bizonata_f_02.jpg')
# pixels = image.load()
# for i in range(image.width):
#                 for j in range(image.height):
#                     if pixels[i, j][:3] not in hex_colors:  # Check if the pixel color is not allowed
#                         pixels[i, j] = (0, 0, 0)  # Set non-matching pixels to black

# image.save('/home/abdulrauf/Projects/MakhiMeter-Training/data/training/model_v1.2/experiment/abc/{0}'.format('D.bizonata_f_02.jpg'))