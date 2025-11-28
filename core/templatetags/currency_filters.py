from django import template

register = template.Library()

@register.filter
def inr_currency(value):
    """Format price as INR currency"""
    try:
        return f"₹{float(value):,.2f}"
    except (ValueError, TypeError):
        return value
