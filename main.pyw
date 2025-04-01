import tkinter as tk
from tkinter import ttk, messagebox # Přidáme messagebox
# import json # Již není potřeba zde
from datetime import datetime
import data_manager # Importujeme nový modul
from add_invoice_window import AddInvoiceWindow # Importujeme okno pro přidání
from invoice_detail_window import InvoiceDetailWindow # Importujeme okno pro detail faktury
from about_window import AboutWindow # Importujeme okno O programu

# --- Hlavní Aplikace ---

class AccountingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Účetní Software")
        self.root.geometry("800x600")

        self.invoices = data_manager.load_invoices() # Použijeme funkci z data_manager

        # Menu Bar
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Faktury", menu=self.file_menu)
        self.file_menu.add_command(label="Přidat fakturu", command=self.open_add_invoice_window)
        self.file_menu.add_command(label="Smazat vybranou fakturu", command=self.delete_selected_invoice)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Konec", command=root.quit)
        
        # Help Menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Nápověda", menu=self.help_menu)
        self.help_menu.add_command(label="O programu", command=self.show_about)

        # Main Frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Invoice Lists Frame
        self.lists_frame = ttk.Frame(self.main_frame)
        self.lists_frame.pack(fill=tk.BOTH, expand=True)
        self.lists_frame.columnconfigure(0, weight=1)
        self.lists_frame.columnconfigure(1, weight=1)
        self.lists_frame.rowconfigure(1, weight=1)

        # Received Invoices
        ttk.Label(self.lists_frame, text="Přijaté faktury", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=(0, 5), sticky="w")
        
        # Treeview pro přijaté faktury
        columns = ('cislo', 'zakaznik', 'datum')
        self.received_tree = ttk.Treeview(self.lists_frame, columns=columns, show='headings', selectmode='browse')
        
        # Definice sloupců
        self.received_tree.heading('cislo', text='Číslo faktury')
        self.received_tree.heading('zakaznik', text='Zákazník')
        self.received_tree.heading('datum', text='Datum')
        
        # Šířky sloupců
        self.received_tree.column('cislo', width=100)
        self.received_tree.column('zakaznik', width=200)
        self.received_tree.column('datum', width=100)
        
        # Umístění treeview
        self.received_tree.grid(row=1, column=0, padx=(0, 5), pady=5, sticky="nsew")
        
        # Scrollbar pro přijaté faktury
        received_scrollbar = ttk.Scrollbar(self.lists_frame, orient=tk.VERTICAL, command=self.received_tree.yview)
        received_scrollbar.grid(row=1, column=0, padx=(0, 5), pady=5, sticky="nse")
        self.received_tree.config(yscrollcommand=received_scrollbar.set)
        
        # Dvojklik na položku
        self.received_tree.bind("<Double-1>", self.show_invoice_detail)

        # Issued Invoices
        ttk.Label(self.lists_frame, text="Vydané faktury", font=("Arial", 12, "bold")).grid(row=0, column=1, pady=(0, 5), sticky="w")
        
        # Treeview pro vydané faktury
        self.issued_tree = ttk.Treeview(self.lists_frame, columns=columns, show='headings', selectmode='browse')
        
        # Definice sloupců
        self.issued_tree.heading('cislo', text='Číslo faktury')
        self.issued_tree.heading('zakaznik', text='Zákazník')
        self.issued_tree.heading('datum', text='Datum')
        
        # Šířky sloupců
        self.issued_tree.column('cislo', width=100)
        self.issued_tree.column('zakaznik', width=200)
        self.issued_tree.column('datum', width=100)
        
        # Umístění treeview
        self.issued_tree.grid(row=1, column=1, padx=(5, 0), pady=5, sticky="nsew")
        
        # Scrollbar pro vydané faktury
        issued_scrollbar = ttk.Scrollbar(self.lists_frame, orient=tk.VERTICAL, command=self.issued_tree.yview)
        issued_scrollbar.grid(row=1, column=1, padx=(5, 0), pady=5, sticky="nse")
        self.issued_tree.config(yscrollcommand=issued_scrollbar.set)
        
        # Dvojklik na položku
        self.issued_tree.bind("<Double-1>", self.show_invoice_detail)

        self.populate_lists()

    def populate_lists(self):
        """Naplní seznamy fakturami."""
        # Vyčistíme seznamy
        for item in self.received_tree.get_children():
            self.received_tree.delete(item)
        for item in self.issued_tree.get_children():
            self.issued_tree.delete(item)
        
        # Uložíme si indexy pro pozdější použití
        self.received_indices = {}
        self.issued_indices = {}

        # Naplníme seznam přijatých faktur
        for idx, invoice in enumerate(self.invoices.get("prijate", [])):
            item_id = self.received_tree.insert('', tk.END, values=(
                invoice.get('cislo', 'N/A'),
                invoice.get('zakaznik', 'N/A'),
                invoice.get('datum', 'N/A')
            ))
            self.received_indices[item_id] = idx

        # Naplníme seznam vydaných faktur
        for idx, invoice in enumerate(self.invoices.get("vydane", [])):
            item_id = self.issued_tree.insert('', tk.END, values=(
                invoice.get('cislo', 'N/A'),
                invoice.get('zakaznik', 'N/A'),
                invoice.get('datum', 'N/A')
            ))
            self.issued_indices[item_id] = idx

    def open_add_invoice_window(self):
        """Otevře okno pro přidání nové faktury."""
        # Předáme self.add_invoice jako callback funkci
        add_window = AddInvoiceWindow(self.root, self.add_invoice)
        add_window.wait_window() # Počkáme, dokud se okno nezavře

    def show_invoice_detail(self, event):
        """Zobrazí detail faktury po dvojkliku."""
        # Zjistíme, který treeview byl kliknut
        tree = event.widget
        selected_item = tree.focus()
        
        if not selected_item:
            return
            
        if tree == self.received_tree:
            invoice_type = "prijate"
            original_index = self.received_indices.get(selected_item)
        elif tree == self.issued_tree:
            invoice_type = "vydane"
            original_index = self.issued_indices.get(selected_item)
        else:
            return
            
        if original_index is not None and invoice_type in self.invoices and original_index < len(self.invoices[invoice_type]):
            invoice_data = self.invoices[invoice_type][original_index]
            InvoiceDetailWindow(self.root, invoice_data, invoice_type, self.update_invoice)
    
    def update_invoice(self, original_data, updated_data, invoice_type):
        """Aktualizuje fakturu v seznamu."""
        # Najdeme index faktury v seznamu
        try:
            invoice_list = self.invoices[invoice_type]
            for i, invoice in enumerate(invoice_list):
                # Porovnáme podle čísla faktury a zákazníka, protože to by mělo být unikátní
                if (invoice.get('cislo') == original_data.get('cislo') and 
                    invoice.get('zakaznik') == original_data.get('zakaznik')):
                    # Nahradíme fakturu aktualizovanými daty
                    self.invoices[invoice_type][i] = updated_data
                    # Uložíme změny
                    data_manager.save_invoices(self.invoices)
                    # Aktualizujeme zobrazení
                    self.populate_lists()
                    return
            
            # Pokud jsme fakturu nenašli, vypíšeme chybu
            print(f"Chyba: Faktura nebyla nalezena v seznamu {invoice_type}")
        except Exception as e:
            print(f"Chyba při aktualizaci faktury: {e}")
            messagebox.showerror("Chyba", f"Nastala chyba při aktualizaci faktury: {e}", parent=self.root)

    def delete_selected_invoice(self):
        """Smaže vybranou fakturu z aktivního seznamu."""
        active_tree = None
        invoice_type = None
        selected_item = None
        original_index = None

        # Zjistíme, který treeview je aktivní (má focus) a má vybranou položku
        focused_widget = self.root.focus_get()
        if focused_widget == self.received_tree:
            active_tree = self.received_tree
            invoice_type = "prijate"
            selected_item = active_tree.focus()
            if selected_item:
                original_index = self.received_indices.get(selected_item)
        elif focused_widget == self.issued_tree:
            active_tree = self.issued_tree
            invoice_type = "vydane"
            selected_item = active_tree.focus()
            if selected_item:
                original_index = self.issued_indices.get(selected_item)

        if active_tree and selected_item and original_index is not None:

            # Ověříme, zda index existuje v seznamu faktur
            if invoice_type not in self.invoices or original_index >= len(self.invoices[invoice_type]):
                 messagebox.showerror("Chyba", "Faktura pro smazání nebyla nalezena (nesoulad indexů).", parent=self.root)
                 return

            invoice_to_delete = self.invoices[invoice_type][original_index]
            invoice_display = f"{invoice_to_delete.get('cislo', 'N/A')} - {invoice_to_delete.get('zakaznik', 'N/A')}"

            confirm = messagebox.askyesno("Potvrdit smazání", f"Opravdu chcete smazat fakturu:\n{invoice_display}?", parent=self.root)

            if confirm:
                try:
                    # Smažeme fakturu z datové struktury podle původního indexu
                    del self.invoices[invoice_type][original_index]
                    # Uložíme změny
                    data_manager.save_invoices(self.invoices)
                    # Aktualizujeme zobrazení v treeview
                    self.populate_lists()
                    messagebox.showinfo("Smazáno", "Faktura byla úspěšně smazána.", parent=self.root)
                except Exception as e:
                    print(f"Chyba při mazání nebo ukládání: {e}")
                    messagebox.showerror("Chyba", f"Nastala chyba při mazání faktury: {e}", parent=self.root)
        else:
            messagebox.showwarning("Nic nevybráno", "Nejprve klikněte na fakturu v seznamu, kterou chcete smazat.", parent=self.root)


    def show_about(self):
        """Zobrazí okno s informacemi o programu."""
        AboutWindow(self.root)
        
    def add_invoice(self, invoice_data, invoice_type):
        """Přidá novou fakturu do seznamu a uloží."""
        if invoice_type == "prijate":
            self.invoices["prijate"].append(invoice_data)
        elif invoice_type == "vydane":
            self.invoices["vydane"].append(invoice_data)
        else:
            print("Neznámý typ faktury")
            return

        data_manager.save_invoices(self.invoices) # Použijeme funkci z data_manager
        self.populate_lists() # Aktualizuje zobrazení

# --- Spuštění aplikace ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AccountingApp(root)
    root.mainloop()
