import pandas as pd
import re
from typing import List, Dict, Any

def validate_csv_structure(df: pd.DataFrame) -> bool:
    """
    Validate that the CSV has the required structure.
    
    Args:
        df: DataFrame to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_columns = [
        'product_id', 'product_name', 'price', 'original_price',
        'description', 'main_category', 'sub_category', 'rating',
        'stock', 'badge', 'offers', 'size_options', 'color_options',
        'image_urls', 'product_url'
    ]
    
    return all(col in df.columns for col in required_columns)

def clean_price(price_str: str) -> float:
    """
    Clean and convert price string to float.
    
    Args:
        price_str: Price as string
        
    Returns:
        Price as float
    """
    if pd.isna(price_str) or price_str == '':
        return 0.0
    
    # Remove currency symbols and extra whitespace
    cleaned = re.sub(r'[^\d.]', '', str(price_str))
    
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def normalize_text(text: str) -> str:
    """
    Normalize text for better search matching.
    
    Args:
        text: Input text
        
    Returns:
        Normalized text
    """
    if pd.isna(text):
        return ''
    
    # Convert to lowercase and remove extra whitespace
    normalized = str(text).lower().strip()
    normalized = re.sub(r'\s+', ' ', normalized)
    
    return normalized

def extract_colors_from_options(color_options: str) -> List[str]:
    """
    Extract individual colors from color options string.
    
    Args:
        color_options: Color options as string (comma-separated)
        
    Returns:
        List of individual colors
    """
    if pd.isna(color_options) or color_options == '':
        return []
    
    # Split by comma and clean each color
    colors = [color.strip().lower() for color in str(color_options).split(',')]
    return [color for color in colors if color]

def format_currency(amount: float) -> str:
    """
    Format currency amount with Indian numbering system.
    
    Args:
        amount: Amount to format
        
    Returns:
        Formatted currency string
    """
    try:
        # Convert to integer to remove decimal places
        amount_int = int(amount)
        
        # Format with commas according to Indian numbering system
        s, *d = str(amount_int).partition(".")
        r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-2:]])
        return r + "".join(d)
    except:
        return str(amount)

def safe_get_value(row: pd.Series, column: str, default: Any = "") -> Any:
    """
    Safely get a value from a DataFrame row.
    
    Args:
        row: DataFrame row
        column: Column name
        default: Default value if column doesn't exist or is null
        
    Returns:
        Value from the row or default
    """
    try:
        value = row[column]
        if pd.isna(value):
            return default
        return value
    except KeyError:
        return default

def calculate_discount_percentage(original_price: float, price: float) -> float:
    """
    Calculate discount percentage.
    
    Args:
        original_price: Original price
        price: Current price
        
    Returns:
        Discount percentage
    """
    if original_price <= 0 or price < 0:
        return 0.0
    
    if original_price <= price:
        return 0.0
    
    discount = original_price - price
    return round((discount / original_price) * 100, 2)

def is_valid_image_url(url: str) -> bool:
    """
    Check if the provided URL is likely a valid image URL.
    
    Args:
        url: Image URL to validate
        
    Returns:
        True if valid, False otherwise
    """
    if pd.isna(url) or url == '':
        return False
    
    url = str(url).strip().lower()
    
    # Common image extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    
    # Check if URL ends with an image extension or contains common image hosting patterns
    return any(ext in url for ext in image_extensions) or any(domain in url for domain in ['imgur.com', 'images.unsplash.com', 'cdn.shopify.com'])

def is_valid_product_url(url: str) -> bool:
    """
    Check if the provided URL is likely a valid product URL.
    
    Args:
        url: Product URL to validate
        
    Returns:
        True if valid, False otherwise
    """
    if pd.isna(url) or url == '':
        return False
    
    url = str(url).strip().lower()
    
    # Check if it's a proper URL
    return url.startswith(('http://', 'https://')) and '.' in url
