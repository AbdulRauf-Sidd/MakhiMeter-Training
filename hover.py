import cv2

def mouse_callback(event, x, y, flags, param):
    global clicked_point
    if event == cv2.EVENT_LBUTTONDOWN:
        file = open('point.txt', "w");
        s = str(x) + "," + str(y);
        file.write(s);
        file.close();
    if event == cv2.EVENT_MOUSEMOVE:
        print(f'x: {x}, y: {y}', image[x][y])
        
# Read the image
image = cv2.imread('test.png', 0)
print(image.shape)
# print(image[293][269]);
# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# image = image.resize((600, 600))

# Create a window and bind the mouse callback function to it
cv2.namedWindow('image')
cv2.setMouseCallback('image', mouse_callback)
high = -1
low = 300;
# for x in range(len(image)):
#     for y in range(len(image[x])):
#         val = image[x][y];
#         if val < low:
#             low = val;
#         if val > high:
#             high = val;

# print(low, high)


# Display the image
cv2.imshow('image', image)

# Wait for the user to close the window
cv2.waitKey(0)
cv2.destroyAllWindows()