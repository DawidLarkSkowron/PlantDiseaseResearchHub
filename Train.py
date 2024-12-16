import tensorflow as tf
from tensorflow.keras.applications import ResNet50, MobileNetV2
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.regularizers import l2
import matplotlib.pyplot as plt
import os

# Parametry treningu
BATCH_SIZE = 32
IMG_SIZE = (224, 224)
INITIAL_EPOCHS = 30
FINE_TUNE_EPOCHS = 10
INITIAL_LEARNING_RATE = 0.0001
FINE_TUNE_LEARNING_RATE = 0.00001
PATIENCE = 10

# Ścieżki do katalogów z danymi (zmień na swoje)
TRAIN_DIR = r'C:\RozpoznawanieWzorców\PlantDiseaseResearchHub\Apple_Train'
VAL_DIR = r'C:\RozpoznawanieWzorców\PlantDiseaseResearchHub\Apple_Val'

# Sprawdzenie, czy katalogi istnieją
if not os.path.exists(TRAIN_DIR) or not os.path.exists(VAL_DIR):
    raise FileNotFoundError("Ścieżki do katalogów treningowych/walidacyjnych są nieprawidłowe.")

# Generatory danych z zaawansowaną augmentacją dla treningu i walidacji
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.3,
    brightness_range=[0.7, 1.3],
    horizontal_flip=True,
    vertical_flip=True,
    fill_mode='nearest'
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

val_generator = val_datagen.flow_from_directory(
    VAL_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

# Budowanie modelu - możliwość wyboru MobileNetV2 dla mniejszych danych
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Dodanie własnych warstw z Dropout i L2 regularizacją
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.5)(x)
x = Dense(512, activation='relu', kernel_regularizer=l2(0.01))(x)
predictions = Dense(train_generator.num_classes, activation='softmax', kernel_regularizer=l2(0.01))(x)

# Kompilacja modelu
model = Model(inputs=base_model.input, outputs=predictions)

# Zamrożenie warstw bazowego modelu
for layer in base_model.layers:
    layer.trainable = False

model.compile(optimizer=Adam(learning_rate=INITIAL_LEARNING_RATE),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Callbacki: EarlyStopping i ModelCheckpoint
early_stopping = EarlyStopping(monitor='val_loss', patience=PATIENCE, restore_best_weights=True)
checkpoint = ModelCheckpoint('best_apple.keras', save_best_only=True, monitor='val_loss')

# Trenowanie modelu
history = model.fit(
    train_generator,
    epochs=INITIAL_EPOCHS,
    validation_data=val_generator,
    callbacks=[early_stopping, checkpoint]
)

# Fine-tuning: odblokowanie ostatnich 20 warstw bazowego modelu
for layer in base_model.layers[-20:]:
    layer.trainable = True

# Kompilacja modelu z niższą stopą uczenia dla fine-tuningu
model.compile(optimizer=Adam(learning_rate=FINE_TUNE_LEARNING_RATE),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Dalsze trenowanie (fine-tuning)
history_fine = model.fit(
    train_generator,
    epochs=FINE_TUNE_EPOCHS,
    validation_data=val_generator,
    callbacks=[early_stopping, checkpoint]
)

# Zapisywanie finalnego modelu
model.save('apple.keras')

# Funkcja do wizualizacji wyników treningu
def plot_training(history, history_fine):
    plt.figure(figsize=(12, 4))

    # Wykres dokładności
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train Accuracy (Initial)')
    plt.plot(history.history['val_accuracy'], label='Val Accuracy (Initial)')
    plt.plot(history_fine.history['accuracy'], label='Train Accuracy (Fine-tuning)')
    plt.plot(history_fine.history['val_accuracy'], label='Val Accuracy (Fine-tuning)')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.title('Train and Validation Accuracy')

    # Wykres straty
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train Loss (Initial)')
    plt.plot(history.history['val_loss'], label='Val Loss (Initial)')
    plt.plot(history_fine.history['loss'], label='Train Loss (Fine-tuning)')
    plt.plot(history_fine.history['val_loss'], label='Val Loss (Fine-tuning)')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.title('Train and Validation Loss')

    plt.show()

# Wizualizacja wyników
plot_training(history, history_fine)
