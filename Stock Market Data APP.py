import tkinter as tk
import requests

API_KEY = "G5PFNBMTQUJCGR7T"
class StockApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Stock Market Data App")
        self.geometry("400x400")
        self.resizable(width=False,height=False)
        # Configure styles
        self.configure(background="#f2f2f2")
        self.label_font = ("Arial", 12, "bold")
        self.entry_font = ("Arial", 12)
        self.button_font = ("Arial", 12, "bold")
        self.text_font = ("Arial", 11)

        self.symbol_label = tk.Label(self, text="Stock Symbol:", font=self.label_font, bg="#f2f2f2")
        self.symbol_label.pack(pady=10)

        self.symbol_entry = tk.Entry(self, font=self.entry_font)
        self.symbol_entry.pack()

        self.get_realtime_button = tk.Button(self, text="Get Real-Time Price", command=self.get_realtime_price,
                                             font=self.button_font, bg="#4CAF50", fg="white", relief="solid")
        self.get_realtime_button.pack(pady=10)

        self.get_historical_button = tk.Button(self, text="Get Historical Prices", command=self.get_historical_prices,
                                               font=self.button_font, bg="#4CAF50", fg="white", relief="solid")
        self.get_historical_button.pack(pady=5)

        self.stock_data_text = tk.Text(self, font=self.text_font, bg="white", height=10)
        self.stock_data_text.pack(pady=10)

    def get_realtime_price(self):
        symbol = self.symbol_entry.get()
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()
        if "Global Quote" in data:
            price = data["Global Quote"]["05. price"]
            self.stock_data_text.delete(1.0, tk.END)
            self.stock_data_text.insert(tk.END, f"Real-Time Price: {price}")
        else:
            self.stock_data_text.delete(1.0, tk.END)
            self.stock_data_text.insert(tk.END, "Error retrieving data.")

    def get_historical_prices(self):
        symbol = self.symbol_entry.get()
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()
        if "Time Series (Daily)" in data:
            time_series = data["Time Series (Daily)"]
            dates = list(time_series.keys())[:10]
            prices = [float(time_series[date]["4. close"]) for date in dates]

            self.stock_data_text.delete(1.0, tk.END)
            self.stock_data_text.insert(tk.END, "Last 10 Days' Closing Prices:\n")
            for date, price in zip(dates, prices):
                self.stock_data_text.insert(tk.END, f"Date: {date}, Price: {price}\n")
        else:
            self.stock_data_text.delete(1.0, tk.END)
            self.stock_data_text.insert(tk.END, "Error retrieving data.")
app = StockApp()
app.mainloop()
