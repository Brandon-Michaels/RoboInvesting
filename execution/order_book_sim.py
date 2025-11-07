import json
import time
from pathlib import Path

# Simple dummy order book (given in spec)
order_book = {
    'AAPL': {'bid': [174.9, 174.8, 174.7], 'ask': [175.1, 175.2, 175.3]},
    'MSFT': {'bid': [318.1, 318.0, 317.9], 'ask': [318.3, 318.4, 318.5]},
}

executed_trades = []

def best_bid(symbol):
    return max(order_book[symbol]['bid'])

def best_ask(symbol):
    return min(order_book[symbol]['ask'])

def market_buy(symbol, qty):
    px = best_ask(symbol)
    executed_trades.append({
        'symbol': symbol,
        'side': 'BUY',
        'qty': qty,
        'price': px,
        'ts': time.time(),
    })

def market_sell(symbol, qty):
    px = best_bid(symbol)
    executed_trades.append({
        'symbol': symbol,
        'side': 'SELL',
        'qty': qty,
        'price': px,
        'ts': time.time(),
    })

if __name__ == "__main__":
    # Run a tiny demo
    market_buy('AAPL', 100)
    market_sell('MSFT', 50)

    # Always write relative to THIS file's folder
    base = Path(__file__).resolve().parent
    out = base / "outputs" / "executed_trades.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump(executed_trades, f, indent=2)

    print(f"Wrote {len(executed_trades)} trades")
    print(f"Saved trades -> {out}")