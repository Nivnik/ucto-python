import json
import os

INVOICES_FILE = 'invoices.json'

def load_invoices():
    """Načte faktury z JSON souboru."""
    if not os.path.exists(INVOICES_FILE):
        # Pokud soubor neexistuje, vytvoříme ho s prázdnou strukturou
        save_invoices({"prijate": [], "vydane": []})
        return {"prijate": [], "vydane": []}
    try:
        with open(INVOICES_FILE, 'r', encoding='utf-8') as f:
            # Zkusíme načíst data, pokud je soubor prázdný, vrátíme prázdnou strukturu
            content = f.read()
            if not content:
                return {"prijate": [], "vydane": []}
            return json.loads(content)
    except json.JSONDecodeError:
        # Pokud je soubor poškozený nebo neobsahuje validní JSON
        print(f"Chyba: Soubor {INVOICES_FILE} je poškozený nebo neobsahuje validní JSON. Vytvářím nový.")
        save_invoices({"prijate": [], "vydane": []})
        return {"prijate": [], "vydane": []}
    except Exception as e:
        print(f"Nastala neočekávaná chyba při načítání faktur: {e}")
        # V případě jiné chyby je bezpečnější vrátit prázdná data
        return {"prijate": [], "vydane": []}


def save_invoices(invoices):
    """Uloží faktury do JSON souboru."""
    try:
        with open(INVOICES_FILE, 'w', encoding='utf-8') as f:
            json.dump(invoices, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Nastala chyba při ukládání faktur: {e}")
