import cv2
image_path = '/home/abdulrauf/Projects/makhi_meter_dataset/version/training/perfect/image0189.png'  # Replace with your image file path
gray_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
gray_image = cv2.equalizeHist(gray_image)
    # Step 2: Convert to binary image using thresholding
_, binary_image = cv2.threshold(gray_image, 39, 255, cv2.THRESH_BINARY)
inverted_image = cv2.bitwise_not(binary_image)

cv2.imwrite('/home/abdulrauf/Projects/makhi_meter_dataset/version/training/perfect binary/image0189.png', inverted_image)
