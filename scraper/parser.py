import re

def clean_text(text):
    if not text:
        return ""
    return text.strip()

def parse_price(price_str, currency_symbol="£"):
    if not price_str:
        return 0.0, currency_symbol
    
    # Remove currency symbol and whitespace
    clean_str = price_str.replace(currency_symbol, "").strip()
    try:
        return float(clean_str), currency_symbol
    except ValueError:
        return 0.0, currency_symbol

def parse_rating(rating_class):
    # Example: ['star-rating', 'Three'] -> 3
    ratings = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
    if not rating_class:
        return 0
    
    for r in rating_class:
        if r in ratings:
            return ratings[r]
    return 0
