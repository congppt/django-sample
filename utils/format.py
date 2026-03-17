import locale

def number(value):
    try:
        return f"{float(value):,.2f}".replace(',', '.')
    except (ValueError, TypeError):
        return "—"

def text(value):
    try:
        return str(value)
    except:
        return "—"

def date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        return "—"

def datetime(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M:%S")
    except (ValueError, TypeError):
        return "—"

def badge(value):
    return f"<span style='background-color: #007bff; color: white; padding: 4px 8px; border-radius: 4px;'>{value}</span>"