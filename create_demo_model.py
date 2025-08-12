import tensorflow as tf
import numpy as np
import os

def create_demo_model():
    """
    Create a simple demo model for testing purposes
    This model will return random predictions but maintains the correct structure
    """
    
    # Create a simple model that mimics MobileNetV2 structure
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(224, 224, 3)),
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64, 3, activation='relu'),
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(4, activation='softmax')
    ])
    
    # Compile the model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Save the model
    model.save('models/kidney_anomaly_model.h5')
    
    print("Demo model created successfully!")
    print("Model saved as: models/kidney_anomaly_model.h5")
    print("\nNote: This is a demo model for testing purposes only.")
    print("For production use, please train the model with real CT scan data.")

if __name__ == "__main__":
    create_demo_model()
