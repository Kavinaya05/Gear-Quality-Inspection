import cv2
import numpy as np

# Read the image
image = cv2.imread("sharp.jpg")



# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, 100, 200)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a blank canvas to draw contours
contour_image = np.zeros_like(image)

# Draw contours on the blank canvas
cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)



cv2.imwrite('contour_img.jpg',contour_image)

# Display the result
cv2.imshow("Original Image", image)
cv2.imshow("Contour Points", contour_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
