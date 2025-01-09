# Updated script to include additional fruits and diseases based on user input

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Paths to models for different plant diseases
MODELS = {
    "Jabłko": r'C:\RozpoznawanieWzorców\PlantDiseaseResearchHub\MODELS\Apple\best_apple.keras',
    #"Pomidor": r'C:\RozpoznawanieWzorców\PlantDiseaseResearchHub\MODELS\Tomato\best_tomato.keras',
    "Kukurydza": r'C:\RozpoznawanieWzorców\PlantDiseaseResearchHub\MODELS\Corn\best_corn.keras',
    "Ziemniak": r'C:\RozpoznawanieWzorców\PlantDiseaseResearchHub\MODELS\Potato\best_potato.keras',
}

# Class categories for each model
CLASS_CATEGORIES = {
    "Jabłko": ["Zdrowy", "Apple Rust", "Apple Scab"],
    "Pomidor": [
        "Tomato Early Blight", "Tomato Late Blight", "Tomato Mosaic Virus",
        "Tomato Yellow Virus", "Tomato Bacterial Spot", "Tomato Septoria Spot",
        "Tomato Mold Leaf"
    ],
    "Kukurydza": ["Gray Leaf Spot", "Corn Rust", "Corn Leaf Blight"],
    "Ziemniak": ["Potato Early Blight", "Potato Late Blight", "Healthy"],
}

# Preload models
loaded_models = {}
for plant, model_path in MODELS.items():
    try:
        loaded_models[plant] = load_model(model_path)
    except Exception as e:
        messagebox.showerror("Błąd ładowania modelu", f"Nie można załadować modelu dla {plant}: {e}")

# Function to choose and display file
def wybierz_plik():
    if not rodzaj_lisci.get():
        messagebox.showwarning("Brak wyboru", "Najpierw wybierz rodzaj liści z listy.")
        return

    sciezka_pliku = filedialog.askopenfilename(
        title="Wybierz obraz liścia",
        filetypes=[("Pliki obrazów", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if sciezka_pliku:
        wyswietl_obraz(sciezka_pliku)
        analizuj_obraz(sciezka_pliku)
    else:
        messagebox.showinfo("Brak pliku", "Nie wybrano żadnego pliku.")

# Function to display the selected image
def wyswietl_obraz(sciezka):
    try:
        obraz = Image.open(sciezka)
        obraz = obraz.resize((500, 500))  # Resize for better window fit
        obraz_tk = ImageTk.PhotoImage(obraz)
        panel_obraz.config(image=obraz_tk)
        panel_obraz.image = obraz_tk
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie można otworzyć pliku: {e}")

# Function to analyze the image with the selected model
def analizuj_obraz(sciezka):
    rodzaj = rodzaj_lisci.get()
    if rodzaj in loaded_models:
        try:
            # Load and preprocess the image
            obraz = Image.open(sciezka).resize((224, 224))
            obraz = np.array(obraz)
            obraz = preprocess_input(obraz)  # Normalize for MobileNetV2
            obraz = np.expand_dims(obraz, axis=0)

            # Prediction with the model
            predictions = loaded_models[rodzaj].predict(obraz)[0]

            # Results in percentages
            categories = CLASS_CATEGORIES[rodzaj]
            wyniki = {categories[i]: f"{predictions[i] * 100:.2f}%" for i in range(len(categories))}
            wynik_tekst = "\n".join([f"{klasa}: {procent}" for klasa, procent in wyniki.items()])

            messagebox.showinfo("Wynik Analizy", wynik_tekst)
        except Exception as e:
            messagebox.showerror("Błąd analizy", f"Wystąpił problem podczas analizy: {e}")
    else:
        messagebox.showinfo("Brak modelu", f"Model dla {rodzaj} nie jest zaimplementowany.")

# Create the main application window
root = tk.Tk()
root.title("Analiza Zdrowia Liści")
root.geometry("500x700")
root.resizable(False, False)

# Title label
label_title = tk.Label(root, text="Sprawdź Zdrowie Liścia", font=("Arial", 20))
label_title.pack(pady=10)

# Dropdown for selecting the plant type
rodzaje_lisci = [
    "Jabłko", "Pomidor", "Kukurydza", "Ziemniak"
]

label_lista = tk.Label(root, text="Wybierz rodzaj liści:", font=("Arial", 12))
label_lista.pack(pady=5)

rodzaj_lisci = ttk.Combobox(root, values=rodzaje_lisci, state="readonly")
rodzaj_lisci.pack(pady=5)
rodzaj_lisci.set("")  # Set default empty value

# Button to select the file
btn_wybierz = tk.Button(root, text="Wybierz obraz liścia", command=wybierz_plik)
btn_wybierz.pack(pady=20)

# Panel to display the image
panel_obraz = tk.Label(root, text="Tutaj pojawi się wybrany obraz", bg="white", width=50, height=20)
panel_obraz.pack(pady=20)

# Run the application
root.mainloop()
