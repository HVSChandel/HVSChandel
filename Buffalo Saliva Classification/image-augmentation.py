import cv2

# Read the image
image = cv2.imread("Non-Estrum.jpg")

# Rotate the image by 180 degrees
rotated_image = cv2.rotate(image, cv2.ROTATE_180)

# Save the rotated image
cv2.imwrite("Non-Estrum_180.jpg", rotated_image)


