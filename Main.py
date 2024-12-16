import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

# Słownik z modelami (dla demonstracji - funkcje zwracające przykładowe wyniki)
def model_jablko():
    return "Wynik analizy: Liść jabłoni jest zdrowy."

def model_papryka():
    return "Wynik analizy: Liść papryki ma oznaki choroby."

def model_jagoda():
    return "Wynik analizy: Liść jagody jest zdrowy."

def model_wisnia():
    return "Wynik analizy: Liść wiśni ma infekcję grzybiczą."

def model_kukurydza():
    return "Wynik analizy: Liść kukurydzy jest zdrowy."

def model_winogron():
    return "Wynik analizy: Liść winorośli ma plamistość liści."

def model_brzoskwinia():
    return "Wynik analizy: Liść brzoskwini jest zdrowy."

def model_ziemniak():
    return "Wynik analizy: Liść ziemniaka ma zarazę ziemniaczaną."

def model_malina():
    return "Wynik analizy: Liść maliny jest zdrowy."

def model_soyabean():
    return "Wynik analizy: Liść soi ma rdze liści."

def model_truskawka():
    return "Wynik analizy: Liść truskawki ma objawy mączniaka."

def model_pomidor():
    return "Wynik analizy: Liść pomidora ma mozaikę wirusową."

# Przypisanie modeli do odpowiednich rodzajów liści
modele = {
    "Jabłko": model_jablko,
    "Papryka": model_papryka,
    "Jagoda": model_jagoda,
    "Wiśnia": model_wisnia,
    "Kukurydza": model_kukurydza,
    "Winogron": model_winogron,
    "Brzoskwinia": model_brzoskwinia,
    "Ziemniak": model_ziemniak,
    "Malina": model_malina,
    "Soyabean": model_soyabean,
    "Truskawka": model_truskawka,
    "Pomidor": model_pomidor,
}

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
    else:
        messagebox.showinfo("Brak pliku", "Nie wybrano żadnego pliku.")

# Funkcja do wyświetlania wybranego obrazu
def wyswietl_obraz(sciezka):
    try:
        obraz = Image.open(sciezka)
        obraz = obraz.resize((400, 400))  # Zmiana rozmiaru dla lepszego dopasowania do okna
        obraz_tk = ImageTk.PhotoImage(obraz)
        panel_obraz.config(image=obraz_tk)
        panel_obraz.image = obraz_tk
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie można otworzyć pliku: {e}")

# Funkcja do analizy obrazu za pomocą odpowiedniego modelu
def analizuj_obraz():
    rodzaj = rodzaj_lisci.get()
    if not rodzaj:
        messagebox.showwarning("Brak wyboru", "Najpierw wybierz rodzaj liści z listy.")
        return

    wynik = modele[rodzaj]()
    messagebox.showinfo("Wynik Analizy", wynik)

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

# Przycisk do analizy obrazu
btn_analizuj = tk.Button(root, text="Analizuj obraz", command=analizuj_obraz)
btn_analizuj.pack(pady=20)

# Uruchomienie aplikacji
root.mainloop()
