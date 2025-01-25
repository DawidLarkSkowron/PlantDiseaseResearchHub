# Updated script to include additional fruits and diseases based on user input

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import tkinter.ttk as ttk
from PIL import Image, ImageTk, ImageOps
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Define color scheme
COLORS = {
    'bg': '#f0f0f0',
    'primary': '#2c3e50',
    'secondary': '#3498db',
    'text': '#2c3e50',
    'accent': '#e74c3c'
}

# Paths to models for different plant diseases
MODELS = {
    "Jabłko": r'MODELS\Apple\best_apple.keras',
    "Kukurydza": r'MODELS\Corn\best_corn.keras',
    "Ziemniak": r'best_potato.keras',
    "Winogrono": r'MODELS\Grape\best_grape.keras',
    "Papryka": r'MODELS\Pepper\best_pepper.keras',
}

# Class categories for each model
CLASS_CATEGORIES = {
    "Jabłko": ["Parch jabłoni", "Zdrowy", "Rdza jabłoni"],
    "Kukurydza": ["Zaraza kukurydzy", "Rdza kukurydzy", "Szara plamistość liści kukurydzy", "Zdrowy"],
    "Ziemniak": ["Wczesna zaraza ziemniaka", "Późna zaraza ziemniaka", "Zdrowy"],
    "Winogrono": ["Zdrowy", "Czarna zgnilizna winorośli"],
    "Papryka": ["Zdrowy", "Bakterioza papryki"]
}

# Preload models
loaded_models = {}
for plant, model_path in MODELS.items():
    try:
        loaded_models[plant] = load_model(model_path)
    except Exception as e:
        messagebox.showerror("Błąd ładowania modelu",
                             f"Nie można załadować modelu dla {plant}: {e}")

# Function to choose and display file


def wybierz_plik():
    if not rodzaj_lisci.get():
        messagebox.showwarning(
            "Brak wyboru", "Najpierw wybierz rodzaj liści z listy.")
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
        # Smaller fixed display size
        DISPLAY_WIDTH = 500
        DISPLAY_HEIGHT = 300

        # Load and convert image
        obraz = Image.open(sciezka)

        # Calculate scaling ratio maintaining aspect ratio
        ratio = min(DISPLAY_WIDTH/obraz.width, DISPLAY_HEIGHT/obraz.height)
        new_size = (int(obraz.width*ratio), int(obraz.height*ratio))

        # Resize image
        obraz = obraz.resize(new_size, Image.LANCZOS)

        # Create background
        background = Image.new(
            'RGB', (DISPLAY_WIDTH, DISPLAY_HEIGHT), COLORS['bg'])

        # Calculate position to paste (center)
        x = (DISPLAY_WIDTH - new_size[0])//2
        y = (DISPLAY_HEIGHT - new_size[1])//2

        # Paste image onto background
        background.paste(obraz, (x, y))

        # Convert to PhotoImage
        obraz_tk = ImageTk.PhotoImage(background)

        # Update label
        panel_obraz.config(image=obraz_tk, text="")
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
            obraz = preprocess_input(obraz)
            obraz = np.expand_dims(obraz, axis=0)

            # Prediction with the model
            predictions = loaded_models[rodzaj].predict(obraz)[0]

            # Results in percentages
            categories = CLASS_CATEGORIES[rodzaj]
            wyniki = {
                categories[i]: f"{predictions[i] * 100:.1f}%"
                for i in range(len(categories))
            }

            # Sort results by percentage
            sorted_results = sorted(
                wyniki.items(),
                key=lambda x: float(x[1].strip('%')),
                reverse=True
            )

            # Update primary result
            primary_result, primary_percent = sorted_results[0]
            if primary_result.lower() == "zdrowy":
                label_primary_wynik.configure(
                    style='PrimaryResult.Healthy.TLabel')
            else:
                label_primary_wynik.configure(
                    style='PrimaryResult.Disease.TLabel')
            label_primary_wynik.config(
                text=f"{primary_result}: {primary_percent}")

            # Update secondary results
            secondary_text = "\n".join(
                [f"{klasa}: {procent}" for klasa, procent in sorted_results[1:]]
            )
            label_secondary_wynik.config(text=secondary_text)

        except Exception as e:
            label_primary_wynik.config(
                text=f"Wystąpił problem podczas analizy")
            label_secondary_wynik.config(text=str(e))
    else:
        label_primary_wynik.config(
            text=f"Model dla {rodzaj} nie jest zaimplementowany")
        label_secondary_wynik.config(text="")


def create_styled_frame(parent, padding=(20, 20)):
    frame = ttk.Frame(parent, padding=padding)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    return frame


# Create the main application window
root = tk.Tk()
root.title("Analiza Zdrowia Liści")
root.geometry("800x800")  # Reduced height
root.resizable(False, False)
root.configure(bg=COLORS['bg'])

style = ttk.Style()
style.configure('TFrame', background=COLORS['bg'])
style.configure('TLabel', background=COLORS['bg'], foreground=COLORS['text'])
style.configure('TButton', padding=10, font=('Segoe UI', 10))
style.configure('Header.TLabel', font=('Segoe UI', 24, 'bold'),
                foreground=COLORS['primary'])
style.configure('SubHeader.TLabel', font=('Segoe UI', 12))
style.configure('Healthy.TLabel',
                font=('Segoe UI', 14, 'bold'),
                foreground='#2ecc71'  # Green
                )
style.configure('Disease.TLabel',
                font=('Segoe UI', 14, 'bold'),
                foreground='#e74c3c'  # Red
                )
style.configure('Results.TLabel',
                font=('Segoe UI', 12),
                justify='center'
                )

# Add new style configurations
style.configure('ResultTitle.TLabel',
                font=('Segoe UI', 18, 'bold'),
                foreground=COLORS['text'],
                justify='center'
                )

style.configure('PrimaryResult.Healthy.TLabel',
                font=('Segoe UI', 16, 'bold'),
                foreground='#2ecc71',
                justify='center'
                )

style.configure('PrimaryResult.Disease.TLabel',
                font=('Segue UI', 16, 'bold'),
                foreground='#e74c3c',
                justify='center'
                )

style.configure('SecondaryResult.TLabel',
                font=('Segoe UI', 10),
                foreground='#95a5a6',
                justify='center'
                )

# Main container
main_frame = create_styled_frame(root)

# Header section
header_frame = create_styled_frame(main_frame)
label_title = ttk.Label(
    header_frame, text="Analiza Zdrowia Liści", style='Header.TLabel')
label_title.pack(pady=(0, 20))

# Selection section
selection_frame = create_styled_frame(main_frame)
label_lista = ttk.Label(
    selection_frame, text="Wybierz rodzaj liści:", style='SubHeader.TLabel')
label_lista.pack(pady=(0, 5))

rodzaje_lisci = [
    "Jabłko", "Kukurydza", "Ziemniak", "Winogrono", "Papryka"
]

rodzaj_lisci = ttk.Combobox(
    selection_frame, values=rodzaje_lisci, state="readonly", width=30)
rodzaj_lisci.pack(pady=(0, 10))
rodzaj_lisci.set("")

btn_wybierz = ttk.Button(
    selection_frame, text="Wybierz obraz liścia", command=wybierz_plik)
btn_wybierz.pack(pady=(10, 0))

# Image display section
image_frame = create_styled_frame(main_frame)
image_frame.configure(relief='groove', borderwidth=1, height=300)
image_frame.pack_propagate(False)  # Prevent frame from expanding
panel_obraz = ttk.Label(
    image_frame,
    text="Wybierz plik aby wyświetlić obraz",
    background=COLORS['bg'],
    anchor='center'
)
panel_obraz.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Results section
results_frame = create_styled_frame(main_frame)
results_frame.configure(height=200)
results_frame.pack_propagate(False)

# Title label
label_title_wynik = ttk.Label(
    results_frame,
    text="Wyniki analizy",
    style='ResultTitle.TLabel',
    justify=tk.CENTER
)
label_title_wynik.pack(pady=(10, 5))

# Primary result label
label_primary_wynik = ttk.Label(
    results_frame,
    text="",
    style='PrimaryResult.Healthy.TLabel',
    justify=tk.CENTER
)
label_primary_wynik.pack(pady=5)

# Secondary results label
label_secondary_wynik = ttk.Label(
    results_frame,
    text="",
    style='SecondaryResult.TLabel',
    justify=tk.CENTER
)
label_secondary_wynik.pack(pady=5)

# Run the application
root.mainloop()
