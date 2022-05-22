from django import template
from cocktails.models import OrderItem

register= template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = OrderItem.objects.filter(user=user, ordered=False)
        if qs.exists():
            count=0
            for item in qs:
                count+=item.quantity
            return count
        return 0
    return 0
