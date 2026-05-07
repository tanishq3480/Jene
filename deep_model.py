import tensorflow as tf
from tensorflow.keras import layers, models

def build_model(input_length):
    model = models.Sequential([
        layers.Embedding(input_dim=4, output_dim=8, input_length=input_length),
        layers.Conv1D(64, 5, activation='relu'),
        layers.MaxPooling1D(2),
        layers.Conv1D(128, 5, activation='relu'),
        layers.GlobalMaxPooling1D(),
        layers.Dense(64, activation='relu'),
        layers.Dense(3, activation='softmax')  # 3 classes
    ])
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model