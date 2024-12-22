from PIL import Image, ImageFilter

# Open an image file
img = Image.open('/home/abdulrauf/Projects/MakhiMeter-Training/test3.png')

# Apply Gaussian blur
blurred_img = img.filter(ImageFilter.GaussianBlur(radius=1))

# Save or display the image
blurred_img.save('blurred_image.png')
blurred_img.show()
