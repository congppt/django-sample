import locale

def currency(value):
    """Format currency using locale settings with Vietnamese Dong symbol"""
    if value is None:
        return "—"
    try:
        # Set locale to Vietnamese for consistent formatting
        # locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')
        # Format with grouping but replace currency symbol with đ
        return locale.currency(value, grouping=True, symbol=False) + "đ"
    except (ValueError, TypeError, locale.Error):
        # Fallback to simple formatting if locale fails
        return f"{float(value):,.2f}".replace(',', '.') + "đ"

