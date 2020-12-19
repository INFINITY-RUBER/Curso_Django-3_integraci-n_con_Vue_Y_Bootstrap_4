from decimal import Decimal
from django.conf import settings
from listelement.models import Element


class Cart(object):

    def __init__(self, request):
        
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        element_ids = self.cart.keys()

        elements = Element.objects.filter(id__in=element_ids)
        cart = self.cart.copy()

        for element in elements:
            cart[str(element.id)]['element'] = element

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum( item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        # precio total

        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def add(self, element, quantity=1, override_quantity=False):
        element_id = str(element.id)

        if element_id  not in self.cart:
            self.cart[element_id] = {'quantity': 0, 'price':str(element.price)}

        if override_quantity:
            self.cart[element_id]['quantity'] = quantity
        else:
            self.cart[element_id]['quantity'] += quantity

        self.save()

    def save(self):
        # marca la sesion como modificada
        self.session.modified = True

    def remove(self, element):
        element_id = str(element.id)

        if element_id in self.cart:
            del self.cart[element_id]

        self.save()

    def getItem(self, element_id):
        element_id = str(element_id)

        if element_id in self.cart:
            return self.cart[element_id]

        return None

    def clear(self):
        del self.session.get[settings.CART_SESSION_ID]
        self.save()