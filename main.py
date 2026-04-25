import tkinter as tk
from tkinter import ttk
import requests
import json
from datetime import datetime

API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://api.exchangerate-api.com/v4/latest/"
HISTORY_FILE = "history.json"

class CurrencyConverter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Currency Converter")
        self.geometry("400x300")

        # Виджеты выбора валюты
        self.from_currency_var = tk.StringVar(value="USD")
        self.to_currency_var = tk.StringVar(value="EUR")

        from_currency_label = ttk.Label(self, text="From:")
        from_currency_label.grid(row=0, column=0, padx=10, pady=10)
        from_currency_combo = ttk.Combobox(self, textvariable=self.from_currency_var)
        from_currency_combo['values'] = ["USD", "EUR", "GBP"]
        from_currency_combo.grid(row=0, column=1, padx=10, pady=10)

        to_currency_label = ttk.Label(self, text="To:")
        to_currency_label.grid(row=1, column=0, padx=10, pady=10)
        to_currency_combo = ttk.Combobox(self, textvariable=self.to_currency_var)
        to_currency_combo['values'] = ["USD", "EUR", "GBP"]
        to_currency_combo.grid(row=1, column=1, padx=10, pady=10)

        # Поле ввода суммы
        amount_label = ttk.Label(self, text="Amount:")
        amount_label.grid(row=2, column=0, padx=10, pady=10)
        self.amount_entry = ttk.Entry(self)
        self.amount_entry.grid(row=2, column=1, padx=10, pady=10)

        # Кнопка конвертации
        convert_button = ttk.Button(self, text="Convert", command=self.convert_currency)
        convert_button.grid(row=3, columnspan=2, padx=10, pady=10)

        # Таблица истории
        history_frame = ttk.Frame(self)
        history_frame.grid(row=4, columnspan=2, sticky='ew')
        columns = ('Date', 'From', 'To', 'Amount', 'Result')
        self.history_treeview = ttk.Treeview(history_frame, columns=columns, show='headings')
        for col in columns:
            self.history_treeview.heading(col, text=col)
        self.history_treeview.pack(fill='both', expand=True)

        # Загрузить историю
        self.load_history()

    def convert_currency(self):
        amount = self.amount_entry.get().strip()
        if not validate_input(amount):
            tk.messagebox.showerror("Invalid Input", "Please enter a valid positive number.")
            return

        from_currency = self.from_currency_var.get()
        to_currency = self.to_currency_var.get()

        exchange_rate = get_exchange_rate(from_currency, to_currency)
        converted_amount = round(float(amount) * exchange_rate, 2)

        # Добавить в историю
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_item = {
            "Date": current_time,
            "From": f"{amount} {from_currency}",
            "To": f"{converted_amount} {to_currency}"
        }
        self.add_to_history(history_item)

        # Показать результат
        tk.messagebox.showinfo("Conversion Result",
                              f"{amount} {from_currency} is equal to {converted_amount} {to_currency}")

    def add_to_history(self, item):
        history_data = load_history()
        history_data.append(item)
        save_history(history_data)

        # Обновить таблицу
        self.history_treeview.insert("", "end", values=(item["Date"], item["From"], item["To"]))

    def load_history(self):
        history_data = load_history()
        for entry in history_data:
            self.history_treeview.insert("", "end", values=(entry["Date"], entry["From"], entry["To"]))

def get_exchange_rate(from_currency, to_currency):
    response = requests.get(BASE_URL + from_currency, params={"apikey": API_KEY})
    data = response.json()
    return data["rates"].get(to_currency, 0)

def validate_input(amount):
    try:
        value = float(amount)
        return value > 0
    except ValueError:
        return False

def save_history(history_data):
    with open(HISTORY_FILE, 'w') as file:
        json.dump(history_data, file)

def load_history():
    try:
        with open(HISTORY_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

if __name__ == "__main__":
    app = CurrencyConverter()
    app.mainloop()
