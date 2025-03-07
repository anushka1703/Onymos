import threading
import random
import time

class Order:
    def __init__(self, order_type, ticker, quantity, price):
        self.order_type = order_type  # "Buy" or "Sell"
        self.ticker = ticker
        self.quantity = quantity
        self.price = price
        self.next = None

class OrderBook:
    def __init__(self):
        self.head = None  # Linked list head
        self.tail = None  # Linked list tail
        self.lock = threading.Lock()

    def add_order(self, order):
        with self.lock:  # Thread safety
            if not self.head:
                self.head = self.tail = order
            else:
                self.tail.next = order
                self.tail = order

    def remove_order(self, prev, order):
        with self.lock:  # Thread safety
            if prev:
                prev.next = order.next
            else:
                self.head = order.next
            if order == self.tail:
                self.tail = prev

class StockExchange:
    def __init__(self):
        self.buy_orders = OrderBook()
        self.sell_orders = OrderBook()

    def add_order(self, order_type, ticker, quantity, price):
        order = Order(order_type, ticker, quantity, price)
        if order_type == "Buy":
            self.buy_orders.add_order(order)
        else:
            self.sell_orders.add_order(order)
        self.match_orders()

    def match_orders(self):
        prev_sell = None
        sell = self.sell_orders.head
        
        while sell:
            prev_buy = None
            buy = self.buy_orders.head
            while buy:
                if buy.price >= sell.price and buy.ticker == sell.ticker:
                    trade_quantity = min(buy.quantity, sell.quantity)
                    print(f"Trade Executed: {trade_quantity} shares of {sell.ticker} at {sell.price}")
                    buy.quantity -= trade_quantity
                    sell.quantity -= trade_quantity
                    
                    if buy.quantity == 0:
                        self.buy_orders.remove_order(prev_buy, buy)
                    if sell.quantity == 0:
                        self.sell_orders.remove_order(prev_sell, sell)
                        break  # Move to next sell order
                    
                prev_buy = buy
                buy = buy.next
            
            prev_sell = sell
            sell = sell.next

# Simulating active stock transactions
def simulate_trading(stock_exchange, num_orders=100):
    tickers = [f"STOCK{i}" for i in range(1024)]
    for _ in range(num_orders):
        order_type = random.choice(["Buy", "Sell"])
        ticker = random.choice(tickers)
        quantity = random.randint(1, 100)
        price = random.randint(10, 500)
        stock_exchange.add_order(order_type, ticker, quantity, price)
        time.sleep(0.01)

# Running the simulation
if __name__ == "__main__":
    exchange = StockExchange()
    simulate_trading(exchange, num_orders=50)
