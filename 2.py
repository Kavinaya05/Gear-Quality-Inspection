


import cv2
import numpy as np
from math import sqrt

# Read the image
image = cv2.imread('contour_img.jpg')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Find contours
contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterate through contours and draw white circles
for contour in contours:
    # Fit a circle to the contour points
    (x, y), radius = cv2.minEnclosingCircle(contour)
    center = (int(x), int(y))
    radius = int(radius)
    
    # Draw the circle on the image
    cv2.circle(image, center, radius, (255, 255, 255), 2)

# Convert the image with drawn circles to grayscale
gray_with_circles = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold the image to isolate the white circles
_, thresh = cv2.threshold(gray_with_circles, 240, 255, cv2.THRESH_BINARY)

# Find contours of the white circles
white_contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

L1 = []
largest_contour = None
largest_area = 0

# Iterate through white contours and draw the red center points
for contour in white_contours:
    # Calculate the moments of the contour
    M = cv2.moments(contour)
    
    # Calculate the centroid of the contour
    if M["m00"] != 0:
        center_x = int(M["m10"] / M["m00"])
        center_y = int(M["m01"] / M["m00"])
        
        L1.append((center_x, center_y))
        
        # Draw the center of the circle in red
        cv2.circle(image, (center_x, center_y), 3, (0, 0, 255), -1)
        
        # Annotate the red point with its coordinates
        cv2.putText(image, f"({center_x}, {center_y})", (center_x + 10, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        # Calculate the area of the contour
        area = cv2.contourArea(contour)
        
        # Check if this is the largest contour
        if area > largest_area:
            largest_area = area
            largest_contour = contour

# Find the center of the largest white circle
if largest_contour is not None:
    M = cv2.moments(largest_contour)
    if M["m00"] != 0:
        largest_center_x = int(M["m10"] / M["m00"])
        largest_center_y = int(M["m01"] / M["m00"])
        largest_center_point = (largest_center_x, largest_center_y)
        print(f"center pt: {largest_center_point}")
        
        # Remove the largest center point from L1 if present
        if largest_center_point in L1:
            L1.remove(largest_center_point)
else:
    print("No contours found")

# Print the list of all center points excluding the largest
print(L1)

# Calculate and print distances
if largest_center_point is not None:
    distances = []
    for point in L1:
        distance = sqrt((largest_center_point[0] - point[0]) ** 2 + (largest_center_point[1] - point[1]) ** 2)
        distances.append(distance)
        print(f"Distance from {largest_center_point} to {point}: {distance:.2f}")
    
    if distances:
        min_distance = min(distances)
        max_distance = max(distances)
        print(f"Smallest distance: {min_distance:.2f}")
        print(f"Largest distance: {max_distance:.2f}")

print('Distance bet center & inner pt :',min_distance*0.0068)
print('Distance bet center & outer pt :',max_distance*0.0068)

print('Diameter of inner circle :',2*min_distance*0.0068)
print('Diameter of outer circle :',2*max_distance*0.0068)

cv2.imwrite('final.jpg', image)
cv2.imshow('Circle Fitted to Contour', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
















