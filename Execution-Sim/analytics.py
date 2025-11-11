from typing import Iterable, Dict, List, Optional
import math

def mean(x: Iterable[float]) -> float:
    x = list(x); 
    return sum(x)/len(x) if x else float("nan")

def median(x: Iterable[float]) -> float:
    x = sorted(x); n = len(x)
    if n == 0: return float("nan")
    m = n//2
    return (x[m-1]+x[m])/2.0 if n%2==0 else x[m]

def variance(x: Iterable[float], sample: bool=False) -> float:
    x = list(x); n=len(x)
    if n==0 or (sample and n<2): return float("nan")
    mu = sum(x)/n
    ss = sum((xi-mu)**2 for xi in x)
    return ss/(n-1 if sample else n)

def stdev(x: Iterable[float], sample: bool=False) -> float:
    v = variance(x, sample=sample)
    return math.sqrt(v) if v==v else float("nan")

def price_stats(prices: Iterable[float], sample: bool=False) -> Dict[str, float]:
    prices = list(prices)
    return {
        "count": len(prices),
        "mean": mean(prices),
        "median": median(prices),
        "variance": variance(prices, sample=sample),
        "stdev": stdev(prices, sample=sample),
    }

def stats_from_order_book(order_book: Dict[str, Dict[str, List[float]]],
                          side: Optional[str]=None,
                          sample: bool=False) -> Dict[str, Dict[str, float]]:
    """
    order_book format: {'AAPL': {'bid':[...], 'ask':[...]}}
    side: 'bid', 'ask', or None to combine both sides.
    """
    out: Dict[str, Dict[str, float]] = {}
    for sym, lvls in order_book.items():
        if side is None:
            prices = list(lvls.get("bid", [])) + list(lvls.get("ask", []))
        else:
            prices = list(lvls.get(side, []))
        out[sym] = price_stats(prices, sample=sample)
    return out
