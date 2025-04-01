import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime

class InvoiceDetailWindow(tk.Toplevel):
    def __init__(self, parent, invoice_data, invoice_type, save_callback):
        super().__init__(parent)
        self.parent = parent
        self.invoice_data = invoice_data.copy()  # Vytvoříme kopii, abychom neměnili originál přímo
        self.invoice_type = invoice_type
        self.save_callback = save_callback  # Funkce pro uložení změn
        self.original_data = invoice_data  # Uchováme originální data pro porovnání
        self.title(f"Detail faktury: {invoice_data.get('cislo', 'N/A')}")
        self.geometry("600x700")  # Zvětšíme okno, aby byla vidět všechna tlačítka
        self.transient(parent)  # Okno bude vždy nad hlavním oknem
        self.grab_set()  # Zamkne interakci s hlavním oknem
        
        # Vytvoření hlavního rámce
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Základní informace o faktuře
        info_frame = ttk.LabelFrame(main_frame, text="Základní informace", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Číslo faktury
        ttk.Label(info_frame, text="Číslo faktury:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.invoice_number_entry = ttk.Entry(info_frame, width=30)
        self.invoice_number_entry.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        self.invoice_number_entry.insert(0, invoice_data.get('cislo', ''))
        
        # Zákazník
        ttk.Label(info_frame, text="Zákazník:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.customer_entry = ttk.Entry(info_frame, width=30)
        self.customer_entry.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        self.customer_entry.insert(0, invoice_data.get('zakaznik', ''))
        
        # Datum
        ttk.Label(info_frame, text="Datum (YYYY-MM-DD):", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.date_entry = ttk.Entry(info_frame, width=30)
        self.date_entry.grid(row=2, column=1, sticky="w", padx=5, pady=2)
        self.date_entry.insert(0, invoice_data.get('datum', ''))
        
        # Položky faktury
        items_frame = ttk.LabelFrame(main_frame, text="Položky faktury", padding="10")
        items_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Tabulka položek
        columns = ('nazev', 'cena')
        self.items_tree = ttk.Treeview(items_frame, columns=columns, show='headings')
        self.items_tree.heading('nazev', text='Název položky')
        self.items_tree.heading('cena', text='Cena (Kč)')
        self.items_tree.column('nazev', width=400)
        self.items_tree.column('cena', width=100, anchor='e')
        self.items_tree.pack(fill=tk.BOTH, expand=True)
        
        # Tlačítka pro správu položek
        buttons_frame = ttk.Frame(items_frame)
        buttons_frame.pack(fill=tk.X, pady=5)
        
        add_item_button = ttk.Button(buttons_frame, text="Přidat položku", command=self.add_item)
        add_item_button.pack(side=tk.LEFT, padx=5)
        
        edit_item_button = ttk.Button(buttons_frame, text="Upravit položku", command=self.edit_item)
        edit_item_button.pack(side=tk.LEFT, padx=5)
        
        delete_item_button = ttk.Button(buttons_frame, text="Smazat položku", command=self.delete_item)
        delete_item_button.pack(side=tk.LEFT, padx=5)
        
        # Scrollbar pro tabulku
        scrollbar = ttk.Scrollbar(items_frame, orient=tk.VERTICAL, command=self.items_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.items_tree.configure(yscrollcommand=scrollbar.set)
        
        # Celková cena
        total_frame = ttk.Frame(items_frame)
        total_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Label(total_frame, text="Celková cena:", font=("Arial", 10, "bold")).pack(side=tk.RIGHT, padx=(0, 10))
        self.total_price_label = ttk.Label(total_frame, text="0.00 Kč", font=("Arial", 10, "bold"))
        self.total_price_label.pack(side=tk.RIGHT)
        
        # Naplnění tabulky položkami
        self.items_list = invoice_data.get('polozky', []).copy()  # Vytvoříme kopii seznamu položek
        self.update_items_tree()
        
        # Poznámka
        notes_frame = ttk.LabelFrame(main_frame, text="Poznámka", padding="10")
        notes_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.notes_text = scrolledtext.ScrolledText(notes_frame, height=4, width=40, wrap=tk.WORD)
        self.notes_text.pack(fill=tk.X)
        self.notes_text.insert(tk.INSERT, invoice_data.get('poznamka', ''))
        
        # Tlačítka
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=(0, 5))
        
        save_button = ttk.Button(buttons_frame, text="Uložit změny", command=self.save_changes)
        save_button.pack(side=tk.LEFT, padx=5)
        
        close_button = ttk.Button(buttons_frame, text="Zavřít bez uložení", command=self.destroy)
        close_button.pack(side=tk.LEFT, padx=5)
    
    def update_items_tree(self):
        """Aktualizuje zobrazení položek v treeview."""
        # Vyčistíme treeview
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        
        # Naplníme treeview položkami
        total_price = 0
        for item in self.items_list:
            price = item.get('cena', 0)
            total_price += price
            self.items_tree.insert('', tk.END, values=(item.get('nazev', 'N/A'), f"{price:.2f}"))
        
        # Aktualizujeme celkovou cenu
        if hasattr(self, 'total_price_label'):
            self.total_price_label.config(text=f"{total_price:.2f} Kč")
    
    def add_item(self):
        """Přidá novou položku do faktury."""
        # Vytvoříme nové okno pro přidání položky
        add_window = tk.Toplevel(self)
        add_window.title("Přidat položku")
        add_window.geometry("400x150")
        add_window.transient(self)
        add_window.grab_set()
        
        # Formulář pro přidání položky
        ttk.Label(add_window, text="Název položky:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        name_entry = ttk.Entry(add_window, width=30)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_window, text="Cena (Kč):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        price_entry = ttk.Entry(add_window, width=30)
        price_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Funkce pro přidání položky
        def add_item_to_list():
            name = name_entry.get().strip()
            price_str = price_entry.get().strip()
            
            if not name:
                messagebox.showwarning("Chybějící název", "Zadejte název položky.", parent=add_window)
                return
            if not price_str:
                messagebox.showwarning("Chybějící cena", "Zadejte cenu položky.", parent=add_window)
                return
            
            try:
                price = float(price_str.replace(',', '.'))  # Povolí desetinnou čárku i tečku
            except ValueError:
                messagebox.showerror("Neplatná cena", "Cena musí být číslo.", parent=add_window)
                return
            
            # Přidáme položku do seznamu
            self.items_list.append({"nazev": name, "cena": price})
            self.update_items_tree()
            add_window.destroy()
        
        # Tlačítka
        button_frame = ttk.Frame(add_window)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        add_button = ttk.Button(button_frame, text="Přidat", command=add_item_to_list)
        add_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = ttk.Button(button_frame, text="Zrušit", command=add_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)
    
    def edit_item(self):
        """Upraví vybranou položku."""
        selected_item = self.items_tree.focus()
        if not selected_item:
            messagebox.showwarning("Nic nevybráno", "Vyberte položku k úpravě.", parent=self)
            return
        
        # Získáme index vybrané položky
        selected_index = self.items_tree.index(selected_item)
        item_data = self.items_list[selected_index]
        
        # Vytvoříme nové okno pro úpravu položky
        edit_window = tk.Toplevel(self)
        edit_window.title("Upravit položku")
        edit_window.geometry("400x150")
        edit_window.transient(self)
        edit_window.grab_set()
        
        # Formulář pro úpravu položky
        ttk.Label(edit_window, text="Název položky:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        name_entry = ttk.Entry(edit_window, width=30)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        name_entry.insert(0, item_data.get('nazev', ''))
        
        ttk.Label(edit_window, text="Cena (Kč):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        price_entry = ttk.Entry(edit_window, width=30)
        price_entry.grid(row=1, column=1, padx=5, pady=5)
        price_entry.insert(0, str(item_data.get('cena', '')))
        
        # Funkce pro uložení úprav
        def save_item_changes():
            name = name_entry.get().strip()
            price_str = price_entry.get().strip()
            
            if not name:
                messagebox.showwarning("Chybějící název", "Zadejte název položky.", parent=edit_window)
                return
            if not price_str:
                messagebox.showwarning("Chybějící cena", "Zadejte cenu položky.", parent=edit_window)
                return
            
            try:
                price = float(price_str.replace(',', '.'))  # Povolí desetinnou čárku i tečku
            except ValueError:
                messagebox.showerror("Neplatná cena", "Cena musí být číslo.", parent=edit_window)
                return
            
            # Aktualizujeme položku v seznamu
            self.items_list[selected_index] = {"nazev": name, "cena": price}
            self.update_items_tree()
            edit_window.destroy()
        
        # Tlačítka
        button_frame = ttk.Frame(edit_window)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        save_button = ttk.Button(button_frame, text="Uložit", command=save_item_changes)
        save_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = ttk.Button(button_frame, text="Zrušit", command=edit_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)
    
    def delete_item(self):
        """Smaže vybranou položku."""
        selected_item = self.items_tree.focus()
        if not selected_item:
            messagebox.showwarning("Nic nevybráno", "Vyberte položku ke smazání.", parent=self)
            return
        
        # Získáme index vybrané položky
        selected_index = self.items_tree.index(selected_item)
        
        # Potvrzení smazání
        confirm = messagebox.askyesno("Potvrdit smazání", "Opravdu chcete smazat tuto položku?", parent=self)
        if confirm:
            # Smažeme položku ze seznamu
            del self.items_list[selected_index]
            self.update_items_tree()
    
    def save_changes(self):
        """Uloží změny faktury."""
        # Získáme data z formuláře
        invoice_number = self.invoice_number_entry.get().strip()
        customer = self.customer_entry.get().strip()
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
        
        # Validace data
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Neplatný formát data", "Datum musí být ve formátu YYYY-MM-DD.", parent=self)
            return
        
        if not self.items_list:
            messagebox.showwarning("Chybějící položky", "Přidejte alespoň jednu položku faktury.", parent=self)
            return
        
        # Vytvoříme nová data faktury
        updated_invoice_data = {
            "cislo": invoice_number,
            "zakaznik": customer,
            "datum": date_str,
            "polozky": self.items_list,
            "poznamka": notes
        }
        
        # Zavoláme callback funkci pro uložení změn
        self.save_callback(self.original_data, updated_invoice_data, self.invoice_type)
        messagebox.showinfo("Uloženo", "Změny byly úspěšně uloženy.", parent=self)
        self.destroy()
