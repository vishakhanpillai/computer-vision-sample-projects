# import cv2
# from deepface import DeepFace
# from gtts import gTTS
# import pygame
# import os
# import time
#
# pygame.mixer.init()
# cap = cv2.VideoCapture(0)
# last_emotion = None
#
# while True:
#     ret, frame = cap.read()
#     results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
#     emotion = results[0]['dominant_emotion']
#
#     cv2.putText(frame,
#                 f'Emotion: {emotion}',
#                 (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
#                 1,
#                 (255, 0, 0),
#                 2)
#
#     if emotion != last_emotion:
#         filename = f"emotion_{int(time.time())}.mp3"
#         tts = gTTS(f"You look {emotion}", lang='en')
#         tts.save(filename)
#
#         pygame.mixer.music.load(filename)
#         pygame.mixer.music.play()
#
#         while pygame.mixer.music.get_busy():
#             time.sleep(0.1)
#
#         pygame.mixer.music.unload()
#         os.remove(filename)
#         last_emotion = emotion
#
#     cv2.imshow('Emotion Recognition', frame)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()

import cv2
from deepface import DeepFace
import pyttsx3
import time

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Set voice to male (usually index 0, but let's find the first male voice)
voices = engine.getProperty('voices')
for voice in voices:
    if 'male' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# Optional: change speaking rate (default ~200)
engine.setProperty('rate', 150)

cap = cv2.VideoCapture(0)
last_emotion = None

while True:
    ret, frame = cap.read()
    results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
    emotion = results[0]['dominant_emotion']

    cv2.putText(frame,
                f'Emotion: {emotion}',
                (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2)

    if emotion != last_emotion:
        print(f"Speaking: You look {emotion}")
        engine.say(f"You look {emotion}")
        engine.runAndWait()
        last_emotion = emotion

    cv2.imshow('Emotion Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
