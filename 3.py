import cv2
import numpy as np
from math import sqrt, cos, sin, pi

# Read the image
image = cv2.imread('contour_img.jpg')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Find contours
contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterate through contours and draw white circles
for contour in contours:
    (x, y), radius = cv2.minEnclosingCircle(contour)
    center = (int(x), int(y))
    radius = int(radius)
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
    M = cv2.moments(contour)
    if M["m00"] != 0:
        center_x = int(M["m10"] / M["m00"])
        center_y = int(M["m01"] / M["m00"])
        L1.append((center_x, center_y))
        cv2.circle(image, (center_x, center_y), 3, (0, 0, 255), -1)
        cv2.putText(image, f"({center_x}, {center_y})", (center_x + 10, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        area = cv2.contourArea(contour)
        if area > largest_area:
            largest_area = area
            largest_contour = contour

# Find the center of the largest white circle
largest_center_point = None
if largest_contour is not None:
    M = cv2.moments(largest_contour)
    if M["m00"] != 0:
        largest_center_x = int(M["m10"] / M["m00"])
        largest_center_y = int(M["m01"] / M["m00"])
        largest_center_point = (largest_center_x, largest_center_y)
        print(f"center pt: {largest_center_point}")
        if largest_center_point in L1:
            L1.remove(largest_center_point)
else:
    print("No contours found")

print(L1)

distances = []
if largest_center_point is not None:
    for point in L1:
        distance = sqrt((largest_center_point[0] - point[0]) ** 2 + (largest_center_point[1] - point[1]) ** 2)
        distances.append((distance, point))

distances.sort()

inner_points = [pt for dist, pt in distances[:len(distances)//2]]
outer_points = [pt for dist, pt in distances[len(distances)//2:]]

# Calculate centroid of inner and outer points
def calculate_centroid(points):
    x_sum = sum(point[0] for point in points)
    y_sum = sum(point[1] for point in points)
    length = len(points)
    return (x_sum // length, y_sum // length) if length > 0 else (0, 0)

inner_centroid = calculate_centroid(inner_points)
outer_centroid = calculate_centroid(outer_points)

# Fit circles to the inner and outer points
if inner_points:
    (x_inner, y_inner), radius_inner = cv2.minEnclosingCircle(np.array(inner_points))
    center_inner = (int(x_inner), int(y_inner))
    radius_inner = int(radius_inner)
    cv2.circle(image, center_inner, radius_inner, (0, 255, 0), 2)  # Green circle for inner layer

if outer_points:
    (x_outer, y_outer), radius_outer = cv2.minEnclosingCircle(np.array(outer_points))
    center_outer = (int(x_outer), int(y_outer))
    radius_outer = int(radius_outer)
    cv2.circle(image, center_outer, radius_outer, (255, 0, 0), 2)  # Blue circle for outer layer

# Calculate the new circle's center and radius
middle_center_x = (center_inner[0] + center_outer[0]) // 2
middle_center_y = (center_inner[1] + center_outer[1]) // 2
middle_center = (middle_center_x, middle_center_y)

middle_radius = (radius_inner + radius_outer) // 2

# Draw the new circle
cv2.circle(image, middle_center, middle_radius, (0, 0, 255), 2)  # Red circle for the middle layer

# Choose an angle (0 radians in this case)
theta = 0

# Calculate a point on the circumference of the red circle
point_x = int(middle_center[0] + middle_radius * cos(theta))
point_y = int(middle_center[1] + middle_radius * sin(theta))
point_on_circumference = (point_x, point_y)

# Draw this point
cv2.circle(image, point_on_circumference, 5, (0, 255, 255), -1)  # Yellow dot for the point on the circumference
cv2.putText(image, f"({point_x}, {point_y})", (point_x + 10, point_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)





# Calculate and print distances to each point
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

print('Distance between center & inner point:', min_distance * 0.0068)
print('Distance between center & outer point:', max_distance * 0.0068)

print('Diameter of inner circle:', 2 * min_distance * 0.0068)
print('Diameter of outer circle:', 2 * max_distance * 0.0068)

# Distance between the pitch circle and center point
distn = sqrt((largest_center_x - point_x) ** 2 + (largest_center_y - point_y) ** 2)

print('Distance between center & pitch circle:', distn * 0.0068)
pd=2*distn*0.0068
print('Diameter of pitch circle:',pd)
rounded_pd = round(pd, 1)
print('Diameter of pitch circle:', rounded_pd)

#addendum
a=1/rounded_pd
print('Addendum:',a)

#circular pitch
P=3.14/rounded_pd
print("circular_pitch : ",P)

#circular thickness
t=0.5*P
print("circular thickness:",t)

#clearance
c=0.157/rounded_pd
print('clearance:',c)

#dedendum
b=1.157/rounded_pd
print('dedendum',b)

#diametral pitch
pitch_d= 16/rounded_pd
print('diametral pitch',pitch_d)

#module
m=25.4/pitch_d
print("module:",m)




# Save and display the final image
cv2.imwrite('pitch.jpg', image)
cv2.imshow('Circle Fitted to Contour', image)
cv2.waitKey(0)
cv2.destroyAllWindows()




