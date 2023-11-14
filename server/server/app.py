# import os
# from flask import Flask, request, render_template, jsonify
# from tensorflow import keras
# import numpy as np
# from PIL import Image
# import tensorflow_hub as hub
# import tensorflow as tf

# app = Flask(__name__)

# # Load your trained image classification model
# #model = keras.models.load_model('20231108-165722-full_data_set_mobilenetv2.h5')
# model = tf.keras.models.load_model(
#        ('20231108-165722-full_data_set_mobilenetv2.h5'),
#        custom_objects={'KerasLayer':hub.KerasLayer}
# )

# # Define a function to preprocess the uploaded image
# def preprocess_image(image_path):
#     img = Image.open(image_path)
#     img = img.resize((224, 224))  # Adjust the size according to your model's input requirements
#     img = np.asarray(img)
#     img = img / 255.0  # Normalize the image data
#     return img

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return jsonify({'error': 'No file part'})
        
#         file = request.files['file']
        
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'})
        
#         if file:
#             # Save the uploaded image
#             image_path = os.path.join('static/upload', file.filename)
#             file.save(image_path)
            
#             # Preprocess the image
#             img = preprocess_image(image_path)
            
#             # Make predictions using your model
#             predictions = model.predict(np.expand_dims(img, axis=0))
            
#             # You can post-process the predictions if needed

#             # Example: Get the class with the highest probability
#             class_idx = np.argmax(predictions)
            
#             # Load a list of class names based on your model
#             class_names = ['Class1', 'Class2', 'Class3']  # Replace with your class names

#             result = class_names[class_idx]

#             return jsonify({'result': result})

#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)

import base64
import numpy as np
import io
import os
from PIL import Image
import keras
from keras import backend as K
from keras.models import Sequential
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
#from keras.preprocessing.image import img_to_array
import tensorflow as tf
import tensorflow_hub as hub

from tensorflow.keras.utils import img_to_array
from flask import request
from flask import jsonify
from flask import Flask

app = Flask(__name__)



def get_model():
    global model
    # model = load_model('20231108-165722-full_data_set_mobilenetv2.h5')
    model = tf.keras.models.load_model(
        ('20231108-165722-full_data_set_mobilenetv2.h5'),
        custom_objects={'KerasLayer':hub.KerasLayer}
 )
    print(" * Model loaded!")

def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    return image

print(" * Loading Keras model...")
get_model()

@app.route("/predict", methods=["POST"])
def predict():
    message = request.get_json(force=True)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    processed_image = preprocess_image(image, target_size=(256, 256))
     
    prediction = model.predict(processed_image).tolist()

    response = {
        'prediction': {
            'dog': prediction[0][0],
            'cat': prediction[0][1]
        }
    }
    return jsonify(response)