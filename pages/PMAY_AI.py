import streamlit as st
import cv2
import numpy as np
import os
from keras.models import load_model
from pygame import mixer

# Initialize the alarm sound
mixer.init()
sound = mixer.Sound('alarm.wav')
# Load the Haar Cascade files for face and eyes detection
face_cascade = cv2.CascadeClassifier('./src/src_for_drow/haar cascade files/haarcascade_frontalface_alt.xml')
left_eye_cascade = cv2.CascadeClassifier('./src/src_for_drow/haar cascade files/haarcascade_lefteye_2splits.xml')
right_eye_cascade = cv2.CascadeClassifier('./src/src_for_drow/haar cascade files/haarcascade_righteye_2splits.xml')

# Load the pre-trained model
model = load_model('./src/src_for_drow/models/cnncat2.h5')

# Define labels
labels = ['Closed', 'Open']

# Streamlit UI
st.title("AI-Based Drowsiness Detection")
st.write("""
This app uses a pre-trained CNN model to detect drowsiness based on eye closure and alert the user with an alarm if necessary.
""")

# Sidebar options
st.sidebar.header("Settings")
threshold = st.sidebar.slider("Sleepiness Threshold", min_value=5, max_value=30, value=15)

# Video streaming
run = st.checkbox('Start Detection')

if run:
    # Open the webcam
    cap = cv2.VideoCapture(0)
    score = 0
    thicc = 2

    # Display webcam feed
    FRAME_WINDOW = st.image([])

    while True:
        ret, frame = cap.read()
        if not ret:
            st.write("Failed to capture video")
            break

        height, width = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces and eyes
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(25, 25))
        left_eye = left_eye_cascade.detectMultiScale(gray)
        right_eye = right_eye_cascade.detectMultiScale(gray)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)

        rpred, lpred = [99], [99]

        for (x, y, w, h) in right_eye:
            r_eye = gray[y:y+h, x:x+w]
            r_eye = cv2.resize(r_eye, (24, 24)) / 255
            r_eye = np.expand_dims(r_eye.reshape(24, 24, -1), axis=0)
            rpred = np.argmax(model.predict(r_eye), axis=1)
            break

        for (x, y, w, h) in left_eye:
            l_eye = gray[y:y+h, x:x+w]
            l_eye = cv2.resize(l_eye, (24, 24)) / 255
            l_eye = np.expand_dims(l_eye.reshape(24, 24, -1), axis=0)
            lpred = np.argmax(model.predict(l_eye), axis=1)
            break

        # Update score and display status
        if rpred[0] == 0 and lpred[0] == 0:
            score += 1
            cv2.putText(frame, "Closed", (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        else:
            score -= 1
            cv2.putText(frame, "Open", (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        if score < 0:
            score = 0
        cv2.putText(frame, f'Score: {score}', (100, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        if score > threshold:
            cv2.putText(frame, "DROWSINESS ALERT!", (200, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            try:
                sound.play()
            except:
                pass
            if thicc < 16:
                thicc += 2
            else:
                thicc = 2
            cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), thicc)

        # Stream the video to Streamlit
        FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Stop detection
        if st.button("Stop"):
            cap.release()
            sound.stop()
            break
