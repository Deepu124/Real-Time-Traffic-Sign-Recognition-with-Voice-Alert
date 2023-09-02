from logging import root
import cv2
import numpy as np
import tensorflow as tf
import pyttsx3
from tensorflow.keras.models import load_model
import threading
import sys
import tkinter as tk
from tkinter import filedialog


# Load the pre-trained model
model = load_model('model.h5')

# Set up video capture
cap = cv2.VideoCapture(0)

# Define a function to preprocess the input image
def preprocess(img):
    # Convert to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Resize to 32x32
    img = cv2.resize(img, (32, 32))
    # Scale pixel values to [0, 1]
    img = img.astype('float32') / 255.0
    # Add a channel dimension
    img = np.expand_dims(img, axis=-1)
    # Return preprocessed image
    return img

# Define a dictionary to map class labels to sign names
sign_names = {
    0: 'Speed limit (20 kilometer per hour)',
    1: 'Speed limit (30 kilometer per hour)',
    2: 'Speed limit (50 kilometer per hour)',
    3: 'Speed limit (60 kilometer per hour)',
    4: 'Speed limit (70 kilometer per hour)',
    5: 'Speed limit (100 kilometer per hour)',
    6: 'End of speed limit (80 kilometer per hour)',
    7: 'Speed limit (80 kilometer per hour)',
    8: 'Speed limit (120 kilometer per hour)',
    9: 'No passing',
    10: 'No passing for vehicles over 3.5 metric tons',
    11: 'Right-of-way at the next intersection',
    12: 'Priority road',
    13: 'Yield',
    14: 'Stop',
    15: 'No vehicles',
    16: 'vehicles over 3.5 metric tons',
    17: 'No entry',
    18: 'General caution',
    19: 'Dangerous curve to the left',
    20: 'Dangerous curve to the right',
    21: 'Double curve',
    22: 'Bumpy road',
    23: 'Slippery road',
    24: 'Road narrows on the right',
    25: 'Road work',
    26: 'Traffic signals',
    27: 'Pedestrians',
    28: 'Children crossing',
    29: 'Bicycles crossing',
    30: 'Beware of ice/snow',
    31: 'Wild animals crossing',
    32: 'End of all speed and passing limits',
    33: 'Turn right ahead',
    34: 'Turn left ahead',
    35: 'Ahead only',
    36: 'Go straight or right',
    37: 'Go straight or left',
    38: 'Keep right',
    39: 'Keep left',
    40: 'Roundabout mandatory',
    41: 'End of no passing',
    42: 'End of no passing by vehicles over 3.5 metric tons'
}

# Set the threshold value for prediction probabilities
threshold = 0.68

# Initialize the text-to-speech engine
engine = pyttsx3.init()


# Define a function to speak the predicted sign name
def speak(sign_name):
    try:
        # Start the engine's event loop
        engine.startLoop(False)

        if sign_name != 'No Sign Detected':
            # Speak the sign name
            engine.say('Predicted traffic sign is ' + sign_name)
            # Get the corresponding sign name
            sign_name = sign_names[label]
            print('Predicted Traffic Sign is :', sign_name)
            


        # Wait for the engine to finish speaking
        engine.iterate()
        engine.endLoop()

    except:
        # Clear the exception information
        sys.exc_info()

# Loop over frames from the video capture
while True:
    # Read a frame from the video capture
    ret, frame = cap.read()

    # Preprocess the input image
    img = preprocess(frame)

    # Make a prediction using the pre-trained model
    pred = model.predict(np.array([img]), verbose=0)


    # Get the predicted class label and probability
    label = np.argmax(pred)
    probability = pred[0][label]

    # Get the corresponding sign name if probability is above threshold; otherwise, classify as "No Sign"
    if probability >= threshold:
        sign_name = sign_names[label]
        # Draw the sign name and probability on the frame
        text = sign_name + ' ({:.2f}%)'.format(probability * 100)
        cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # Display the sign name on the terminal
        print('Predicted Traffic Sign is:', sign_name)
    else:
        sign_name = 'No Sign Detected'

    # Create a new thread to speak the sign name
    speak_thread = threading.Thread(target=speak, args=(sign_name,))
    speak_thread.start()

    # Display the frame
    cv2.imshow('Traffic Sign Detector', frame)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
def quit():
        cap.release()
        cv2.destroyAllWindows()
        sys.exit(0)
    

