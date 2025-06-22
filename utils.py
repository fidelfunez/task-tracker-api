from datetime import datetime
import logging

def parse_date(date_string):
    """
    Parse date string in YYYY-MM-DD format to date object
    
    Args:
        date_string (str): Date string in YYYY-MM-DD format
    
    Returns:
        datetime.date or None: Parsed date object or None if invalid
    """
    try:
        return datetime.strptime(date_string, '%Y-%m-%d').date()
    except (ValueError, TypeError) as e:
        logging.error(f"Date parsing error: {str(e)}")
        return None

def format_date(date_obj):
    """
    Format date object to YYYY-MM-DD string
    
    Args:
        date_obj (datetime.date): Date object to format
    
    Returns:
        str: Formatted date string or None if invalid
    """
    try:
        if date_obj:
            return date_obj.strftime('%Y-%m-%d')
        return None
    except (ValueError, TypeError, AttributeError) as e:
        logging.error(f"Date formatting error: {str(e)}")
        return None

def validate_pagination_params(page, per_page, max_per_page=100):
    """
    Validate pagination parameters
    
    Args:
        page (int): Page number
        per_page (int): Items per page
        max_per_page (int): Maximum allowed items per page
    
    Returns:
        tuple: Validated (page, per_page) values
    """
    try:
        page = max(1, int(page) if page else 1)
        per_page = max(1, min(int(per_page) if per_page else 10, max_per_page))
        return page, per_page
    except (ValueError, TypeError):
        return 1, 10

def sanitize_string(input_string, max_length=None):
    """
    Sanitize string input by stripping whitespace and limiting length
    
    Args:
        input_string (str): String to sanitize
        max_length (int): Maximum allowed length
    
    Returns:
        str: Sanitized string
    """
    if not isinstance(input_string, str):
        return ''
    
    sanitized = input_string.strip()
    
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized
