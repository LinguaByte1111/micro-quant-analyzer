import heapq
from dataclasses import dataclass, field
from typing import List


@dataclass
class Order:
    id: int
    side: str        # BUY or SELL
    price: float
    quantity: int


@dataclass
class Trade:
    buy_order_id: int
    sell_order_id: int
    price: float
    quantity: int


class OrderBook:
    """
    Python simulation of C++ matching engine.
    Production version: cpp/matching_engine.cpp
    Uses same logic — priority queue based order matching.
    """

    def __init__(self):
        self.bids = []  # max heap (negate price)
        self.asks = []  # min heap
        self.trades: List[Trade] = []
        self.trade_count = 0

    def submit_order(self, order: Order):
        if order.side == "BUY":
            heapq.heappush(self.bids, (-order.price, order.id, order))
        else:
            heapq.heappush(self.asks, (order.price, order.id, order))
        self._match_orders()

    def _match_orders(self):
        while self.bids and self.asks:
            best_bid = self.bids[0][2]
            best_ask = self.asks[0][2]

            if best_bid.price >= best_ask.price:
                matched_qty = min(best_bid.quantity, best_ask.quantity)
                trade_price = best_ask.price

                trade = Trade(
                    buy_order_id=best_bid.id,
                    sell_order_id=best_ask.id,
                    price=trade_price,
                    quantity=matched_qty
                )
                self.trades.append(trade)
                self.trade_count += 1

                print(f"  TRADE #{self.trade_count}"
                      f" | Price: {trade_price:.2f}"
                      f" | Qty: {matched_qty}"
                      f" | BuyID: {best_bid.id}"
                      f" | SellID: {best_ask.id}")

                heapq.heappop(self.bids)
                heapq.heappop(self.asks)

                # Partial fills
                if best_bid.quantity > matched_qty:
                    partial = Order(best_bid.id, "BUY",
                                    best_bid.price,
                                    best_bid.quantity - matched_qty)
                    heapq.heappush(self.bids, (-partial.price, partial.id, partial))

                if best_ask.quantity > matched_qty:
                    partial = Order(best_ask.id, "SELL",
                                    best_ask.price,
                                    best_ask.quantity - matched_qty)
                    heapq.heappush(self.asks, (partial.price, partial.id, partial))
            else:
                break

    def print_book(self):
        print(f"\n=== ORDER BOOK SNAPSHOT ===")
        print(f"  Total Trades Matched: {self.trade_count}")
        print(f"  Pending Bids:         {len(self.bids)}")
        print(f"  Pending Asks:         {len(self.asks)}")


def run_simulator():
    print("=== Exchange Simulator (Python) ===")
    print("Production engine: cpp/matching_engine.cpp\n")

    book = OrderBook()

    orders = [
        Order(1,  "BUY",  2450.00, 100),
        Order(2,  "SELL", 2448.00, 80),
        Order(3,  "BUY",  2449.00, 50),
        Order(4,  "SELL", 2451.00, 120),
        Order(5,  "BUY",  2452.00, 200),
        Order(6,  "SELL", 2447.00, 60),
        Order(7,  "BUY",  2446.00, 150),
        Order(8,  "SELL", 2450.00, 90),
        Order(9,  "BUY",  2453.00, 75),
        Order(10, "SELL", 2445.00, 110),
    ]

    print("--- Submitting Orders ---")
    for order in orders:
        print(f"Submitting {order.side}"
                f" | Price: {order.price}"
                f" | Qty: {order.quantity}")
        book.submit_order(order)

    book.print_book()
    return book


if __name__ == "__main__":
    run_simulator()