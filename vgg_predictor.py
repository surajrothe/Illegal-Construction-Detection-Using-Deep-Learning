import tensorflow as tf
import os
from tensorflow.keras.applications.vgg19 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.preprocessing.image import ImageDataGenerator

test_data_dir = 'D:/College_CP/SDM_CP/test'
img_width, img_height = 224, 224
batch_size = 32

test_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

test_generator = test_datagen.flow_from_directory(
    test_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=False)


def predict_class_vgg(image_path):
    # Load the model
    model = load_model('models/vgg19.h5')

    # Load the image
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img)
    img_array = preprocess_input(img_array)
    img_array = img_array.reshape((1, 224, 224, 3))

    # Make a prediction
    prediction = model.predict(img_array)

    # Get the class labels
    class_labels = list(test_generator.class_indices.keys())

    # Print the selected class and confidence score
    predicted_class = class_labels[prediction.argmax()]
    confidence_score = prediction[0][prediction.argmax()]
    print(f"The image is predicted to be {predicted_class} with a confidence score of {confidence_score:.2f}")

    # Save the predicted image
    import matplotlib.pyplot as plt
    plt.imshow(img)
    plt.axis('off')
    save_path = os.path.join('static', 'predicted_images_vgg', 'predicted.jpg')
    plt.savefig(save_path)

    return predicted_class, confidence_score
