from PIL import Image
import numpy as np
import cv2

# Open the binary image, convert to grayscale, and resize it
# img_rgb = Image.open('image0188.png').convert('L').resize((256, 256))

# # Convert the image to a NumPy array and add a channel dimension

# img_rgb = np.array(img_rgb)
# # Convert back to a PIL image
# img_to_save = Image.fromarray(img_rgb)
# # img_to_save = Image.fromarray(img_rgb.squeeze())
# # Save the image
# img_to_save.save('new.png')
# # cv2.imwrite('new.png', img_to_save)

# img_rgb = Image.open('new.png')
# img_rgb = np.array(img_rgb)
# print(img_rgb.shape)


import cv2
import numpy as np

# Read the image using OpenCV in grayscale mode
img_rgb = cv2.imread('image0188.png', cv2.IMREAD_GRAYSCALE)

# Resize the image to 256x256
img_rgb = cv2.resize(img_rgb, (256, 256))

# Optionally add a channel dimension to make the shape (256, 256, 1)
img_rgb = img_rgb.reshape((256, 256, 1))

# Save the image using OpenCV
cv2.imwrite('new.png', img_rgb)

# Read the saved image to confirm the changes
img_rgb = cv2.imread('new.png', cv2.IMREAD_GRAYSCALE)
img_rgb = np.array(img_rgb)
print(img_rgb.shape)  # Should print (256, 256)
