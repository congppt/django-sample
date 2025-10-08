from django import template

register = template.Library()

@register.filter
def get_attribute(object, key):
    """Get item from dictionary by key"""
    if isinstance(object, dict):
        return object.get(key, '')
    return getattr(object, key, '')

@register.filter
def get_badge_color(value):
    """Get appropriate badge color based on value"""
    color_map = {
        'Active': 'green',
        'Inactive': 'red',
        'Pending': 'yellow',
        'Admin': 'purple',
        'Manager': 'blue',
        'User': 'gray',
        'Engineering': 'blue',
        'Marketing': 'pink',
        'Sales': 'green',
        'HR': 'yellow',
        'Finance': 'indigo',
    }
    return color_map.get(value, 'gray')
