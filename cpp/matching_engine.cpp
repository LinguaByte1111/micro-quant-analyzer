#include <iostream>
#include <vector>
#include <queue>
#include <string>
#include <iomanip>

// Order structure
struct Order {
    int id;
    std::string side;   // "BUY" or "SELL"
    double price;
    int quantity;
};

// Trade structure
struct Trade {
    int buy_order_id;
    int sell_order_id;
    double price;
    int quantity;
};

// Order Book
class OrderBook {
private:
    // Max heap for bids (highest price first)
    std::priority_queue<std::pair<double,Order>> bids;
    // Min heap for asks (lowest price first)
    std::priority_queue<std::pair<double,Order>,
        std::vector<std::pair<double,Order>>,
        std::greater<std::pair<double,Order>>> asks;

    std::vector<Trade> trades;
    int trade_count = 0;

public:
    void submit_order(Order order) {
        if (order.side == "BUY") {
            bids.push({order.price, order});
        } else {
            asks.push({order.price, order});
        }
        match_orders();
    }

    void match_orders() {
        while (!bids.empty() && !asks.empty()) {
            Order best_bid = bids.top().second;
            Order best_ask = asks.top().second;

            // Match condition: bid price >= ask price
            if (best_bid.price >= best_ask.price) {
                int matched_qty = std::min(best_bid.quantity, best_ask.quantity);
                double trade_price = best_ask.price;

                Trade trade = {
                    best_bid.id,
                    best_ask.id,
                    trade_price,
                    matched_qty
                };
                trades.push_back(trade);
                trade_count++;

                std::cout << "  TRADE #" << trade_count
                          << " | Price: " << std::fixed << std::setprecision(2) << trade_price
                          << " | Qty: " << matched_qty
                          << " | BuyID: " << best_bid.id
                          << " | SellID: " << best_ask.id
                          << std::endl;

                bids.pop();
                asks.pop();

                // Resubmit partial fills
                if (best_bid.quantity > matched_qty) {
                    Order partial = best_bid;
                    partial.quantity -= matched_qty;
                    bids.push({partial.price, partial});
                }
                if (best_ask.quantity > matched_qty) {
                    Order partial = best_ask;
                    partial.quantity -= matched_qty;
                    asks.push({partial.price, partial});
                }
            } else {
                break;
            }
        }
    }

    void print_book() {
        std::cout << "\n=== ORDER BOOK SNAPSHOT ===" << std::endl;
        std::cout << "Total Trades Matched: " << trade_count << std::endl;
        std::cout << "Pending Bids:  " << bids.size() << std::endl;
        std::cout << "Pending Asks:  " << asks.size() << std::endl;
    }

    int get_trade_count() { return trade_count; }
};

int main() {
    std::cout << "=== AlphaGrep Exchange Simulator ===" << std::endl;
    std::cout << "Simulating NSE Order Book\n" << std::endl;

    OrderBook book;

    // Simulate orders — RELIANCE.NS style prices
    std::vector<Order> orders = {
        {1,  "BUY",  2450.00, 100},
        {2,  "SELL", 2448.00, 80},
        {3,  "BUY",  2449.00, 50},
        {4,  "SELL", 2451.00, 120},
        {5,  "BUY",  2452.00, 200},
        {6,  "SELL", 2447.00, 60},
        {7,  "BUY",  2446.00, 150},
        {8,  "SELL", 2450.00, 90},
        {9,  "BUY",  2453.00, 75},
        {10, "SELL", 2445.00, 110}
    };

    std::cout << "--- Submitting Orders ---" << std::endl;
    for (auto& order : orders) {
        std::cout   << "Submitting " << order.side
                    << " | Price: " << order.price
                    << " | Qty: " << order.quantity << std::endl;
        book.submit_order(order);
    }

    book.print_book();
    return 0;
}