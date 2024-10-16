import cv2

# Step 1: Read the image in grayscale
image_path = '/home/abdulrauf/Projects/makhi_meter_dataset/version/training/perfect/image0184.png'  # Replace with your image file path
gray_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Step 2: Convert to binary image using thresholding
_, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
inverted_image = cv2.bitwise_not(binary_image)

# Step 3: Apply dilation and erosion
# Define the kernel size
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# Dilation
dilated_image = cv2.dilate(inverted_image, kernel, iterations=1)

eroded_image = cv2.erode(dilated_image, kernel, iterations=2)


# Erosion

# Step 4: Save the processed image
cv2.imwrite('processed_image.jpg', eroded_image)  # Saves the image to the current directory

print("Image processing complete and saved as 'processed_image.jpg'")
