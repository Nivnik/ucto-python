import tkinter as tk
from tkinter import ttk

class AboutWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("O programu")
        self.geometry("400x200")
        self.transient(parent)  # Okno bude vždy nad hlavním oknem
        self.grab_set()  # Zamkne interakci s hlavním oknem
        self.resizable(False, False)  # Zakáže změnu velikosti okna
        
        # Vytvoření hlavního rámce
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo nebo ikona (můžete nahradit vlastním obrázkem)
        title_label = ttk.Label(main_frame, text="Účetní Software", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Informace o programu
        info_text = "Účetní program naprogramovala AI ve Visual Studio Code Cline"
        info_label = ttk.Label(main_frame, text=info_text, wraplength=350, justify="center")
        info_label.pack(pady=10)
        
        # Verze
        version_label = ttk.Label(main_frame, text="Verze 1.0", font=("Arial", 8))
        version_label.pack(pady=(10, 0))
        
        # Tlačítko zavřít
        close_button = ttk.Button(main_frame, text="Zavřít", command=self.destroy)
        close_button.pack(pady=10)
