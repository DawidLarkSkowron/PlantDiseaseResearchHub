import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Ścieżki do modeli dla różnych rodzajów liści
MODELS = {
    "Jabłko": r'C:\RozpoznawanieWzorców\PlantDiseaseResearchHub\MODELS\Apple\best_apple.keras'
}

# Kategorie klas dla modelu Apple (dostosuj do swoich klas)
APPLE_CLASSES = ["Zdrowy", "Apple Rust", "Apple Scab"]

# Załaduj model dla jabłka
try:
    apple_model = load_model(MODELS["Jabłko"])
except Exception as e:
    messagebox.showerror("Błąd ładowania modelu", f"Nie można załadować modelu: {e}")

# Funkcja do wyboru pliku i wyświetlenia obrazu
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

# Funkcja do wyświetlania wybranego obrazu
def wyswietl_obraz(sciezka):
    try:
        obraz = Image.open(sciezka)
        obraz = obraz.resize((500, 500))  # Zmiana rozmiaru dla lepszego dopasowania do okna
        obraz_tk = ImageTk.PhotoImage(obraz)
        panel_obraz.config(image=obraz_tk)
        panel_obraz.image = obraz_tk
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie można otworzyć pliku: {e}")

# Funkcja do analizy obrazu za pomocą odpowiedniego modelu
def analizuj_obraz(sciezka):
    rodzaj = rodzaj_lisci.get()
    if rodzaj == "Jabłko":
        try:
            # Załaduj obraz i przetwórz go
            obraz = Image.open(sciezka).resize((224, 224))
            obraz = np.array(obraz)
            obraz = preprocess_input(obraz)  # Normalizacja dla MobileNetV2
            obraz = np.expand_dims(obraz, axis=0)

            # Predykcja za pomocą modelu
            predictions = apple_model.predict(obraz)[0]

            # Wyniki w procentach
            wyniki = {APPLE_CLASSES[i]: f"{predictions[i] * 100:.2f}%" for i in range(len(APPLE_CLASSES))}
            wynik_tekst = "\n".join([f"{klasa}: {procent}" for klasa, procent in wyniki.items()])

            messagebox.showinfo("Wynik Analizy", wynik_tekst)
        except Exception as e:
            messagebox.showerror("Błąd analizy", f"Wystąpił problem podczas analizy: {e}")
    else:
        messagebox.showinfo("Brak modelu", "Model dla tego rodzaju liści nie jest jeszcze zaimplementowany.")

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Analiza Zdrowia Liści")
root.geometry("500x700")
root.resizable(False, False)

# Etykieta tytułowa
label_title = tk.Label(root, text="Sprawdź Zdrowie Liścia", font=("Arial", 20))
label_title.pack(pady=10)

# Lista rozwijana z rodzajami liści
rodzaje_lisci = [
    "Jabłko", "Papryka", "Jagoda", "Wiśnia", "Kukurydza", "Winogron",
    "Brzoskwinia", "Ziemniak", "Malina", "Soyabean", "Truskawka", "Pomidor"
]

label_lista = tk.Label(root, text="Wybierz rodzaj liści:", font=("Arial", 12))
label_lista.pack(pady=5)

rodzaj_lisci = ttk.Combobox(root, values=rodzaje_lisci, state="readonly")
rodzaj_lisci.pack(pady=5)
rodzaj_lisci.set("")  # Ustawienie domyślnej pustej wartości

# Przycisk do wyboru pliku
btn_wybierz = tk.Button(root, text="Wybierz obraz liścia", command=wybierz_plik)
btn_wybierz.pack(pady=20)

# Panel do wyświetlania obrazu
panel_obraz = tk.Label(root, text="Tutaj pojawi się wybrany obraz", bg="white", width=50, height=20)
panel_obraz.pack(pady=20)

# Uruchomienie aplikacji
root.mainloop()
