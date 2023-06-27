"""
MIT License

Copyright (c) 2019 Victor Zhou

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical

def setup():
    # Build the model
    model = Sequential([
        Dense(64, activation='relu', input_shape=(784,)),
        Dense(64, activation='relu'),
        Dense(10, activation='softmax', ),
    ])

    # Fetch the data using mnist
    test_images = mnist.test_images()
    test_labels = mnist.test_labels()
    train_images = mnist.train_images()
    train_labels = mnist.train_labels()

    # Normalize the images (changes grayscale to form that the machine can understand)
    test_images = (test_images / 255) - 0.5
    train_images = (train_images / 255) - 0.5

    # Flatten the images (merges multiple lists into one list)
    test_images = test_images.reshape((-1, 784))
    train_images = train_images.reshape((-1, 784))

    # Configure the model
    model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy'],
    )

    # Train the model
    model.fit(
        train_images, # training data
        to_categorical(train_labels), # training targets
        epochs=5,
        batch_size=32,
    )

    # Test the model
    model.evaluate(
        test_images,
        to_categorical(test_labels)
    )

    # Save the model weights for later use in model.h5
    model.save_weights('model.h5')