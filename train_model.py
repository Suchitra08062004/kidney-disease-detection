import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def create_model(num_classes=4):
    """
    Create MobileNetV2 model with transfer learning for kidney anomaly classification
    """
    # Load pre-trained MobileNetV2
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=(224, 224, 3)
    )
    
    # Freeze the base model layers
    base_model.trainable = False
    
    # Create new model on top
    inputs = tf.keras.Input(shape=(224, 224, 3))
    
    # Preprocessing layer
    x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
    
    # Pass through base model
    x = base_model(x, training=False)
    
    # Add custom layers
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.2)(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.3)(x)
    outputs = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs, outputs)
    
    return model

def prepare_data_generators(data_dir, batch_size=32):
    """
    Prepare data generators for training and validation
    """
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=0.2
    )
    
    # Only rescaling for validation
    val_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )
    
    # Training generator
    train_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical',
        subset='training'
    )
    
    # Validation generator
    val_generator = val_datagen.flow_from_directory(
        data_dir,
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'
    )
    
    return train_generator, val_generator

def train_model(data_dir, epochs=50, batch_size=32):
    """
    Train the kidney anomaly detection model
    """
    # Create model
    model = create_model()
    
    # Compile model
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Prepare data generators
    train_generator, val_generator = prepare_data_generators(data_dir, batch_size)
    
    # Create callbacks
    checkpoint = ModelCheckpoint(
        'models/kidney_anomaly_model.h5',
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    )
    
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True,
        verbose=1
    )
    
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.2,
        patience=5,
        min_lr=1e-7,
        verbose=1
    )
    
    # Train the model
    history = model.fit(
        train_generator,
        epochs=epochs,
        validation_data=val_generator,
        callbacks=[checkpoint, early_stopping, reduce_lr],
        verbose=1
    )
    
    return model, history

def fine_tune_model(model, data_dir, epochs=20, batch_size=16):
    """
    Fine-tune the model by unfreezing some layers
    """
    # Unfreeze the top layers of the base model
    base_model = model.layers[2]  # MobileNetV2 layer
    base_model.trainable = True
    
    # Freeze all the layers before the last 30 layers
    for layer in base_model.layers[:-30]:
        layer.trainable = False
    
    # Recompile the model with a lower learning rate
    model.compile(
        optimizer=Adam(learning_rate=1e-5),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Prepare data generators
    train_generator, val_generator = prepare_data_generators(data_dir, batch_size)
    
    # Create callbacks
    checkpoint = ModelCheckpoint(
        'models/kidney_anomaly_model_finetuned.h5',
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    )
    
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True,
        verbose=1
    )
    
    # Fine-tune the model
    history = model.fit(
        train_generator,
        epochs=epochs,
        validation_data=val_generator,
        callbacks=[checkpoint, early_stopping],
        verbose=1
    )
    
    return model, history

def plot_training_history(history):
    """
    Plot training history
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Plot accuracy
    ax1.plot(history.history['accuracy'], label='Training Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    
    # Plot loss
    ax2.plot(history.history['loss'], label='Training Loss')
    ax2.plot(history.history['val_loss'], label='Validation Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('training_history.png')
    plt.show()

def create_sample_data_structure():
    """
    Create sample data directory structure
    """
    data_dir = 'data/kidney_ct_scans'
    classes = ['Normal', 'Cyst', 'Stone', 'Tumor']
    
    for class_name in classes:
        class_dir = os.path.join(data_dir, class_name)
        os.makedirs(class_dir, exist_ok=True)
        print(f"Created directory: {class_dir}")
    
    print("\nPlease place your CT scan images in the appropriate class folders:")
    print("data/kidney_ct_scans/Normal/ - for normal kidney images")
    print("data/kidney_ct_scans/Cyst/ - for cyst images")
    print("data/kidney_ct_scans/Stone/ - for kidney stone images")
    print("data/kidney_ct_scans/Tumor/ - for tumor images")

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs('models', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # Create sample data structure
    create_sample_data_structure()
    
    # Check if data directory exists and has images
    data_dir = 'data/kidney_ct_scans'
    if not os.path.exists(data_dir):
        print(f"Data directory {data_dir} does not exist. Please create it and add your CT scan images.")
        exit(1)
    
    # Check if there are images in the data directory
    total_images = 0
    for class_name in ['Normal', 'Cyst', 'Stone', 'Tumor']:
        class_dir = os.path.join(data_dir, class_name)
        if os.path.exists(class_dir):
            images = [f for f in os.listdir(class_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            total_images += len(images)
            print(f"{class_name}: {len(images)} images")
    
    if total_images == 0:
        print("No images found in the data directory. Please add CT scan images before training.")
        exit(1)
    
    print(f"\nTotal images found: {total_images}")
    print("Starting model training...")
    
    # Train the model
    model, history = train_model(data_dir, epochs=30, batch_size=32)
    
    # Fine-tune the model
    print("\nStarting fine-tuning...")
    model, history_finetune = train_model(data_dir, epochs=15, batch_size=16)
    
    # Plot training history
    plot_training_history(history)
    
    print("\nTraining completed! Model saved as 'backend/models/kidney_anomaly_model.h5'")
    print("You can now run the Flask application.")
