from rembg import remove
from PIL import Image
import io

# Load your image (replace 'input_image.jpg' with your file path)
input_path = '/home/abdulrauf/Projects/MakhiMeter-Training/image0199.tif'
output_path = 'output_image2.png'

with open(input_path, 'rb') as input_file:
    input_image = input_file.read()

# Remove the background
output_image = remove(input_image)

img = Image.open(io.BytesIO(output_image))
img = img.convert('L')  # Convert to grayscale (mode 'L' for grayscale)

    # Save the processed image with the same name as input
img.save(output_path)

# Save the output image
# with open(output_path, 'wb') as output_file:
#     output_file.write(output_image)

# # Optionally, you can also open and display the image using PIL (Pillow)
# output_image_pil = Image.open(io.BytesIO(output_image))
# output_image_pil.show()
