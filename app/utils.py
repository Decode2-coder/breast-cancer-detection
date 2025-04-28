from tensorflow.keras.preprocessing import image
import numpy as np

def process_image(img_path, patient_addr=None):
    """
    Loads and preprocesses the image for prediction.
    """
    img = image.load_img(img_path, target_size=(224, 224))  # Match model input
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize
    return img_array
