from decimal import Decimal
from django.test import TestCase
from restaurant.models import Menu

class MenuModelTests(TestCase):
    def test_menu_representation(self):
        item = Menu.objects.create(title='Ice cream', price=Decimal('8.50'), inventory=20)
        item.refresh_from_db()
        self.assertEqual(item.get_item(), 'Ice cream : 8.50')
        self.assertEqual(str(item), 'Ice cream : 8.50')
