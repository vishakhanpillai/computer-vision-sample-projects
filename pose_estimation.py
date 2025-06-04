import time
import cv2
import mediapipe as mp
import winsound
import smtplib
from email.message import EmailMessage
import ssl

def send_email_with_attachment(image_path, sender_email, sender_password, receiver_email):
    msg = EmailMessage()
    msg['Subject'] = 'Human Detected - Screenshot'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content('A human was detected by the camera. See the attached screenshot.')

    with open(image_path, 'rb') as f:
        img_data = f.read()
        msg.add_attachment(img_data, maintype='image', subtype='jpeg', filename='screenshot.jpg')

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)
    print("Email sent!")

mpPose = mp.solutions.pose
pose = mpPose.Pose()

mpDraw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

last_screenshot_time = 0
cooldown_seconds = 10

SENDER_EMAIL = 'vishakhanpillaidev@gmail.com'
SENDER_PASSWORD = 'hycb dspl fury jzue'
RECEIVER_EMAIL = 'pillaivishakhan@gmail.com'

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    imageRgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(imageRgb)
    if results.pose_landmarks:
        current_time = time.time()
        if current_time - last_screenshot_time > cooldown_seconds:
            print("human detected!!!")
            winsound.Beep(1000, 200)
            filename = f"screenshot_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame)
            last_screenshot_time = current_time

            send_email_with_attachment(filename, SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL)
        mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
    cv2.imshow('Pose Estimation', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()