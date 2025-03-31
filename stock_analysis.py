import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

def get_stock_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    """Fetch stock data using yfinance"""
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        return df
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

def calculate_technical_indicators(df: pd.DataFrame) -> Dict[str, float]:
    """Calculate technical indicators for a stock"""
    if df.empty:
        return {}
    
    # Calculate SMA
    sma_20 = df['Close'].rolling(window=20).mean().iloc[-1]
    sma_50 = df['Close'].rolling(window=50).mean().iloc[-1]
    
    # Calculate RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs)).iloc[-1]
    
    # Calculate MACD
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    
    return {
        'sma_20': sma_20,
        'sma_50': sma_50,
        'rsi': rsi,
        'macd': macd.iloc[-1],
        'macd_signal': signal.iloc[-1]
    }

def get_fundamental_metrics(ticker: str) -> Dict[str, float]:
    """Get fundamental metrics for a stock"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return {
            'pe_ratio': info.get('forwardPE', 0),
            'price_to_book': info.get('priceToBook', 0),
            'debt_to_equity': info.get('debtToEquity', 0),
            'profit_margins': info.get('profitMargins', 0),
            'return_on_equity': info.get('returnOnEquity', 0)
        }
    except Exception as e:
        print(f"Error fetching fundamental data for {ticker}: {e}")
        return {}

def calculate_stock_score(ticker: str) -> Tuple[float, Dict[str, float]]:
    """Calculate overall stock score based on technical and fundamental analysis"""
    # Get data
    df = get_stock_data(ticker)
    technical = calculate_technical_indicators(df)
    fundamental = get_fundamental_metrics(ticker)
    
    if not technical or not fundamental:
        return 0.0, {}
    
    # Technical score (0-50 points)
    technical_score = 0
    
    # RSI scoring
    if 30 <= technical['rsi'] <= 70:
        technical_score += 20
    elif 20 <= technical['rsi'] <= 80:
        technical_score += 10
    
    # MACD scoring
    if technical['macd'] > technical['macd_signal']:
        technical_score += 15
    
    # Moving average scoring
    if df['Close'].iloc[-1] > technical['sma_20'] > technical['sma_50']:
        technical_score += 15
    
    # Fundamental score (0-50 points)
    fundamental_score = 0
    
    # PE ratio scoring
    if 0 < fundamental['pe_ratio'] < 20:
        fundamental_score += 15
    elif 0 < fundamental['pe_ratio'] < 30:
        fundamental_score += 10
    
    # Profit margins scoring
    if fundamental['profit_margins'] > 0.2:
        fundamental_score += 15
    elif fundamental['profit_margins'] > 0.1:
        fundamental_score += 10
    
    # Return on equity scoring
    if fundamental['return_on_equity'] > 0.15:
        fundamental_score += 20
    elif fundamental['return_on_equity'] > 0.1:
        fundamental_score += 10
    
    total_score = technical_score + fundamental_score
    
    return total_score, {
        'technical_score': technical_score,
        'fundamental_score': fundamental_score,
        'technical_indicators': technical,
        'fundamental_metrics': fundamental
    }

def rank_stocks(tickers: List[str]) -> List[Tuple[str, float, Dict[str, float]]]:
    """Rank a list of stocks based on their scores"""
    stock_scores = []
    for ticker in tickers:
        score, details = calculate_stock_score(ticker)
        stock_scores.append((ticker, score, details))
    
    # Sort by score in descending order
    return sorted(stock_scores, key=lambda x: x[1], reverse=True)

if __name__ == "__main__":
    # Test with some S&P 500 companies
    test_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
    rankings = rank_stocks(test_tickers)
    
    print("\nStock Rankings:")
    print("-" * 50)
    for ticker, score, details in rankings:
        print(f"\n{ticker}:")
        print(f"Total Score: {score}/100")
        print(f"Technical Score: {details['technical_score']}/50")
        print(f"Fundamental Score: {details['fundamental_score']}/50")
        print("\nTechnical Indicators:")
        for key, value in details['technical_indicators'].items():
            print(f"{key}: {value:.2f}")
        print("\nFundamental Metrics:")
        for key, value in details['fundamental_metrics'].items():
            print(f"{key}: {value:.2f}") 