import cv2



# Create a VideoCapture object to access the webcam
cap = cv2.VideoCapture(0)  # 0 indicates the default camera (usually the built-in webcam)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

image_count = 0

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read a frame.")
        break

    # Display the captured frame
    cv2.imshow('Webcam Image Capture', frame)

    # Check for key presses
    key = cv2.waitKey(1) & 0xFF

    # Save the image when the 's' key is pressed
    if key == ord('s'):
        image_count += 1
        image_filename = f"captured_image_{image_count}.jpg"
        cv2.imwrite(image_filename, frame)
        print(f"Saved {image_filename}")

    # Break the loop and release the camera when the 'q' key is pressed
    if key == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
