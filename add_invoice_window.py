import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

class AddInvoiceWindow(tk.Toplevel):
    def __init__(self, parent, app_callback):
        super().__init__(parent)
        self.parent = parent
        self.app_callback = app_callback # Funkce pro předání dat zpět hlavní aplikaci
        self.title("Přidat novou fakturu")
        self.geometry("500x600") # Upravená velikost pro více polí
        self.transient(parent) # Okno bude vždy nad hlavním oknem
        self.grab_set() # Zamkne interakci s hlavním oknem

        # --- Proměnné ---
        self.invoice_type_var = tk.StringVar(value="prijate") # Výchozí typ faktury
        self.items_list = [] # Seznam pro ukládání položek faktury

        # --- GUI Elementy ---
        form_frame = ttk.Frame(self, padding="10")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Číslo faktury
        ttk.Label(form_frame, text="Číslo faktury:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.invoice_number_entry = ttk.Entry(form_frame, width=40)
        self.invoice_number_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # Zákazník
        ttk.Label(form_frame, text="Zákazník:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.customer_entry = ttk.Entry(form_frame, width=40)
        self.customer_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # Typ faktury
        ttk.Label(form_frame, text="Typ faktury:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="Přijatá", variable=self.invoice_type_var, value="prijate").grid(row=2, column=1, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="Vydaná", variable=self.invoice_type_var, value="vydane").grid(row=2, column=2, padx=5, pady=5, sticky="w")

        # Datum
        ttk.Label(form_frame, text="Datum (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = ttk.Entry(form_frame, width=40)
        self.date_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d')) # Předvyplnění aktuálního data

        # --- Položky faktury ---
        items_frame = ttk.LabelFrame(form_frame, text="Položky faktury", padding="10")
        items_frame.grid(row=4, column=0, columnspan=3, padx=5, pady=10, sticky="ew")
        items_frame.columnconfigure(0, weight=3)
        items_frame.columnconfigure(1, weight=2)

        ttk.Label(items_frame, text="Název položky:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.item_name_entry = ttk.Entry(items_frame)
        self.item_name_entry.grid(row=1, column=0, padx=5, pady=2, sticky="ew")

        ttk.Label(items_frame, text="Cena položky:").grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.item_price_entry = ttk.Entry(items_frame)
        self.item_price_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        add_item_button = ttk.Button(items_frame, text="Přidat položku", command=self.add_item)
        add_item_button.grid(row=1, column=2, padx=5, pady=2)

        # Seznam přidaných položek
        self.items_listbox = tk.Listbox(items_frame, height=5)
        self.items_listbox.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        items_scrollbar = ttk.Scrollbar(items_frame, orient=tk.VERTICAL, command=self.items_listbox.yview)
        items_scrollbar.grid(row=2, column=3, padx=(0,5), pady=5, sticky="ns")
        self.items_listbox.config(yscrollcommand=items_scrollbar.set)

        remove_item_button = ttk.Button(items_frame, text="Odebrat vybranou", command=self.remove_item)
        remove_item_button.grid(row=3, column=0, columnspan=3, pady=5)


        # Poznámka
        ttk.Label(form_frame, text="Poznámka:").grid(row=5, column=0, padx=5, pady=5, sticky="nw")
        self.notes_text = scrolledtext.ScrolledText(form_frame, height=4, width=40, wrap=tk.WORD)
        self.notes_text.grid(row=5, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # Tlačítka
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=10)

        save_button = ttk.Button(button_frame, text="Uložit fakturu", command=self.save_invoice)
        save_button.pack(side=tk.LEFT, padx=5)

        cancel_button = ttk.Button(button_frame, text="Zrušit", command=self.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

        form_frame.columnconfigure(1, weight=1) # Umožní roztažení entry polí

    def add_item(self):
        """Přidá položku do seznamu položek."""
        name = self.item_name_entry.get().strip()
        price_str = self.item_price_entry.get().strip()

        if not name:
            messagebox.showwarning("Chybějící název", "Zadejte název položky.", parent=self)
            return
        if not price_str:
            messagebox.showwarning("Chybějící cena", "Zadejte cenu položky.", parent=self)
            return

        try:
            price = float(price_str.replace(',', '.')) # Povolí desetinnou čárku i tečku
        except ValueError:
            messagebox.showerror("Neplatná cena", "Cena musí být číslo.", parent=self)
            return

        item_data = {"nazev": name, "cena": price}
        self.items_list.append(item_data)
        self.items_listbox.insert(tk.END, f"{name} - {price:.2f} Kč") # Zobrazíme v listboxu

        # Vyčistíme pole pro další položku
        self.item_name_entry.delete(0, tk.END)
        self.item_price_entry.delete(0, tk.END)
        self.item_name_entry.focus() # Zaměříme se zpět na název

    def remove_item(self):
        """Odebere vybranou položku ze seznamu."""
        selected_indices = self.items_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Nic nevybráno", "Vyberte položku k odebrání.", parent=self)
            return

        # Odebereme od konce, abychom nenarušili indexy
        for index in reversed(selected_indices):
            self.items_listbox.delete(index)
            del self.items_list[index]

    def save_invoice(self):
        """Získá data z formuláře a předá je zpět hlavní aplikaci."""
        invoice_number = self.invoice_number_entry.get().strip()
        customer = self.customer_entry.get().strip()
        invoice_type = self.invoice_type_var.get()
        date_str = self.date_entry.get().strip()
        notes = self.notes_text.get("1.0", tk.END).strip()

        # Základní validace
        if not invoice_number:
            messagebox.showwarning("Chybějící údaj", "Zadejte číslo faktury.", parent=self)
            return
        if not customer:
            messagebox.showwarning("Chybějící údaj", "Zadejte zákazníka.", parent=self)
            return
        if not date_str:
             messagebox.showwarning("Chybějící údaj", "Zadejte datum.", parent=self)
             return
        # Validace data (jednoduchá kontrola formátu)
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Neplatný formát data", "Datum musí být ve formátu YYYY-MM-DD.", parent=self)
            return

        if not self.items_list:
             messagebox.showwarning("Chybějící položky", "Přidejte alespoň jednu položku faktury.", parent=self)
             return

        invoice_data = {
            "cislo": invoice_number,
            "zakaznik": customer,
            "datum": date_str,
            "polozky": self.items_list, # Uložíme seznam položek
            "poznamka": notes
        }

        # Zavoláme funkci z hlavní aplikace pro uložení
        self.app_callback(invoice_data, invoice_type)
        self.destroy() # Zavřeme okno po uložení
