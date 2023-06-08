from PIL import Image
import numpy as np

def image_to_vector(file):
    # Get image from file
    image = Image.open(file)
    # Change image to correct format
    image = image.convert("L").resize((28, 28))

    # Change image to vector
    vector = np.asarray(image)
    # Normalize
    vector = (vector / 255) - 0.5
    # Flatten
    vector = vector.reshape((-1, 784))

    return vector