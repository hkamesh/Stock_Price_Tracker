import tkinter as tk
from tkinter import messagebox, Frame, Scrollbar, Listbox
import yfinance as yf
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from newsapi import NewsApiClient

# Initialize News API (replace with your API key)
NEWS_API_KEY = '7293da7015764014b18e10e2e6ad7a77'
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# Function to fetch stock prices
def fetch_stock_prices():
    stock_symbols = entry.get().upper().split(",")
    stock_prices.clear()
    for symbol in stock_symbols:
        try:
            stock = yf.Ticker(symbol.strip())
            price = stock.history(period="1d")['Close'].iloc[-1]
            stock_prices[symbol.strip()] = f"${price:.2f}"
            plot_stock(symbol.strip())
        except Exception as e:
            stock_prices[symbol.strip()] = "Invalid Symbol"
    update_stock_list()
    fetch_news()

# Function to update the stock list display
def update_stock_list():
    stock_listbox.delete(0, tk.END)
    for symbol, price in stock_prices.items():
        stock_listbox.insert(tk.END, f"{symbol}: {price}")

# Function to auto-refresh stock prices
def refresh_prices():
    while True:
        time.sleep(5)
        fetch_stock_prices()

# Function to plot stock price trend
def plot_stock(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1mo")
    if data.empty:
        return
    
    ax.clear()
    ax.plot(data.index, data['Close'], label=f"{symbol} Price", color="#3498DB", linewidth=2)
    ax.set_title(f"{symbol} Stock Price (1 Month)", fontsize=12, color="#FFFFFF")
    ax.set_xlabel("Date", fontsize=10, color="#FFFFFF")
    ax.set_ylabel("Price ($)", fontsize=10, color="#FFFFFF")
    ax.legend()
    ax.grid(True, color="#555555", linestyle="--", linewidth=0.5)
    canvas.draw()

# Function to fetch financial news
def fetch_news():
    symbol = entry.get().split(",")[0].strip()
    if not symbol:
        return
    
    try:
        articles = newsapi.get_everything(q=symbol, language='en', sort_by='publishedAt', page=1)
        news_listbox.delete(0, tk.END)
        for article in articles['articles'][:5]:
            title = article['title']
            url = article['url']
            news_listbox.insert(tk.END, f"{title} - {url}")
    except Exception as e:
        news_listbox.insert(tk.END, "Failed to fetch news")

# GUI Setup
root = tk.Tk()
root.title("Multi Stock Price Tracker")
root.geometry("800x600")
root.configure(bg="#1C1C1C")

# Header Frame
header_frame = Frame(root, bg="#2C3E50", height=50)
header_frame.pack(fill="x")
header_label = tk.Label(header_frame, text="Multi Stock Price Tracker", font=("Arial", 20, "bold"), bg="#2C3E50", fg="white")
header_label.pack(pady=5)

# Input Frame
input_frame = Frame(root, bg="#1C1C1C")
input_frame.pack(pady=10)

label = tk.Label(input_frame, text="Enter Stock Symbols (comma-separated):", font=("Arial", 12), bg="#1C1C1C", fg="#FFFFFF")
label.pack(side="left", padx=5)

entry = tk.Entry(input_frame, font=("Arial", 14), width=30, bg="#34495E", fg="#FFFFFF", insertbackground="#FFFFFF", relief="flat")
entry.pack(side="left", padx=5)

button = tk.Button(input_frame, text="Fetch Prices", command=fetch_stock_prices, font=("Arial", 12), bg="#27AE60", fg="white", relief="flat", padx=10, pady=5, activebackground="#2ECC71")
button.pack(side="left", padx=5)

# Stock List Display
list_frame = Frame(root, bg="#1C1C1C")
list_frame.pack(pady=5, fill="both", expand=True)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

stock_listbox = Listbox(list_frame, font=("Arial", 14), bg="#1C1C1C", fg="#FFFFFF", selectbackground="#2ECC71", selectforeground="#FFFFFF", relief="flat", yscrollcommand=scrollbar.set)
stock_listbox.pack(fill="both", expand=True)
scrollbar.config(command=stock_listbox.yview)

# Graph Frame
graph_frame = Frame(root, bg="#1C1C1C", relief="flat", borderwidth=0)
graph_frame.pack(pady=10, fill="both", expand=True)

fig, ax = plt.subplots(figsize=(5, 3), facecolor="#1C1C1C")
ax.set_facecolor("#1C1C1C")
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack()

# News Feed Frame
news_frame = Frame(root, bg="#1C1C1C")
news_frame.pack(pady=5, fill="both", expand=True)

news_label = tk.Label(news_frame, text="Latest News", font=("Arial", 14), bg="#1C1C1C", fg="#FFFFFF")
news_label.pack()

news_scrollbar = Scrollbar(news_frame)
news_scrollbar.pack(side="right", fill="y")

news_listbox = Listbox(news_frame, font=("Arial", 12), bg="#1C1C1C", fg="#FFFFFF", selectbackground="#2ECC71", selectforeground="#FFFFFF", relief="flat", yscrollcommand=news_scrollbar.set)
news_listbox.pack(fill="both", expand=True)
news_scrollbar.config(command=news_listbox.yview)

# Dictionary to store stock prices
stock_prices = {}

# Start background thread for auto-refresh
refresh_thread = threading.Thread(target=refresh_prices, daemon=True)
refresh_thread.start()

# Run the GUI
root.mainloop()
