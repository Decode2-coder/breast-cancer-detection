import os
import pathlib
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# Force CPU execution
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Custom function used inside the model
@tf.keras.utils.register_keras_serializable()
def rgb_to_grayscale(images):
    return tf.image.rgb_to_grayscale(images)

# === MODEL CONFIG ===
MODEL_PATH = pathlib.Path(__file__).parent / "converted_model"
_model = None

from keras.layers import TFSMLayer

def _get_model():
    global _model
    if _model is None:
        print("✓ Loading model using TFSMLayer...")
        _model = tf.keras.Sequential([
            TFSMLayer(
                str(MODEL_PATH),
                call_endpoint="serve"  # or "serving_default" if that was printed
            )
        ])
    return _model


def predict_image(image_tensor, image_type, threshold: float = 0.5):
    # Convert PyTorch-like tensor (with .permute) if applicable
    if hasattr(image_tensor, "numpy"):
        image_np = (
            image_tensor.squeeze(0)
            .permute(1, 2, 0)
            .numpy()
        )
        image_np = np.expand_dims(image_np, axis=0)
    else:
        image_np = image_tensor

    image_np = image_np.astype("float32")
    model = _get_model()
    preds = model.predict(image_np, verbose=0)

    # Choose correct output head
    output_key = {
        "histopathology": "histo_output",
        "mammography": "mammo_output",
        "ultrasound": "ultra_output"
    }.get(image_type.lower())

    if not output_key or not isinstance(preds, dict):
        raise ValueError(f"Invalid output format or image type: {image_type}")

    score = float(preds[output_key][0][0])
    label = "Malignant" if score >= threshold else "Benign"
    return label, round(score * 100, 2)
