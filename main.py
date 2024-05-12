import cv2
import mediapipe as mp
import requests
import time

# Set camera resolution
# CAM_WIDTH = 640
# CAM_HEIGHT = 480

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode


# Create a gesture recognizer instance with the live stream mode:
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    if len(result.gestures) == 2:
        hand1 = result.gestures[0][0].category_name
        hand2 = result.gestures[1][0].category_name
        print(hand1, hand2)
        if hand1 == "Thumb_Up" and hand2 == "Thumb_Up":
            requests.get("http://192.168.50.190:3000/lock-computer")


options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands=2,
    result_callback=print_result)

with GestureRecognizer.create_from_options(options) as recognizer:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        now_in_ms = int(time.time() * 1000)
        recognizer.recognize_async(mp_image, now_in_ms)
        time.sleep(0.15)  # Adjust this value to control the processing speed

        # Display the frame
        # cv2.imshow('MediaPipe Hands', frame)
        #
        # Press 'q' to quit
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

cap.release()
cv2.destroyAllWindows()
