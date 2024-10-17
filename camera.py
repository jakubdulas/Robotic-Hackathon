import cv2

# Start the webcam (default camera is index 0)
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Could not open the camera.")
    exit()

# Loop to continuously get frames
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If the frame is not received correctly, break the loop
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Display the resulting frame
    cv2.imshow("Camera Feed", frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the capture and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()
