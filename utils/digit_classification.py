from keras.models import Sequential
from keras.layers import Dense
from utils.digit_classification_setup import setup
from utils.image_to_vector import image_to_vector
import numpy as np
import os

def digit_classification(image):
    # Build the model
    model = Sequential([
        Dense(64, activation='relu', input_shape=(784,)),
        Dense(64, activation='relu'),
        Dense(10, activation='softmax', ),
    ])

    # Creates model, if it doesn't exist
    if os.path.exists("model.h5") == False:
        print("Creating a new model")
        setup()

    # Load saved weights into the model.
    model.load_weights('model.h5')

    # Use function to change image to vector
    data = image_to_vector(image)

    # Get prediction from model
    prediction = model.predict(data)

    # Change it to readable result
    result = np.argmax(prediction, axis=1)[0]

    return result