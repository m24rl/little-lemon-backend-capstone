from datetime import timedelta
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from restaurant.models import Menu, Booking

User = get_user_model()

class RestaurantAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.customer = User.objects.create_user('customer', password='ValidPassphrase2026!')
        cls.other = User.objects.create_user('other', password='ValidPassphrase2026!')
        cls.staff = User.objects.create_user('staff', password='ValidPassphrase2026!', is_staff=True)
        cls.menu = Menu.objects.create(title='Pasta',price='12.50',inventory=20)

    def authenticate(self,user):
        token,_ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_home_and_public_menu(self):
        self.assertContains(self.client.get('/'), 'Little Lemon')
        self.assertContains(self.client.get('/'), '/static/restaurant/site.css')
        response = self.client.get('/restaurant/menu/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['results'][0]['title'],'Pasta')
        self.assertEqual(self.client.get(f'/restaurant/menu/{self.menu.pk}/').status_code,200)

    def test_menu_write_permissions_and_validation(self):
        payload = {'title':'Salad','price':'9.50','inventory':5}
        self.assertEqual(self.client.post('/restaurant/menu/',payload).status_code,401)
        self.authenticate(self.customer)
        self.assertEqual(self.client.post('/restaurant/menu/',payload).status_code,403)
        self.authenticate(self.staff)
        invalid = {**payload,'price':'-1.00'}
        self.assertEqual(self.client.post('/restaurant/menu/',invalid).status_code,400)
        response = self.client.post('/restaurant/menu/',payload)
        self.assertEqual(response.status_code,201)
        item_id = response.data['id']
        detail = f'/restaurant/menu/{item_id}/'
        self.assertEqual(self.client.put(detail,{**payload,'price':'10.00'}).status_code,200)
        self.assertEqual(Menu.objects.get(pk=item_id).price,Decimal('10.00'))
        self.assertEqual(self.client.patch(detail,{'inventory':0}).status_code,200)
        self.assertEqual(self.client.delete(detail).status_code,204)
        self.assertEqual(self.client.get(detail).status_code,404)

    def test_registration_login_and_revocation(self):
        response = self.client.post('/auth/users/', {'username':'newcustomer','email':'customer@example.test',
            'password':'LemonStrongPassphrase2026!','re_password':'LemonStrongPassphrase2026!'})
        self.assertEqual(response.status_code,201,response.data)
        user = User.objects.get(username='newcustomer')
        self.assertFalse(user.is_staff)
        self.assertNotEqual(user.password,'LemonStrongPassphrase2026!')
        login = self.client.post('/auth/token/login/',{'username':'newcustomer','password':'LemonStrongPassphrase2026!'})
        self.assertEqual(login.status_code,200,login.data)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+login.data['auth_token'])
        self.assertEqual(self.client.get('/restaurant/booking/tables/').status_code,200)
        self.assertEqual(self.client.post('/auth/token/logout/').status_code,204)
        self.assertEqual(self.client.get('/restaurant/booking/tables/').status_code,401)

    def test_booking_crud_and_owner_is_server_assigned(self):
        payload = {'name':'Ada','no_of_guests':2,'booking_date':(timezone.now()+timedelta(days=10)).isoformat(), 'user':self.other.pk}
        path = '/restaurant/booking/tables/'
        self.assertEqual(self.client.get(path).status_code,401)
        self.assertEqual(self.client.post(path,payload).status_code,401)
        self.authenticate(self.customer)
        response = self.client.post(path,payload)
        self.assertEqual(response.status_code,201,response.data)
        booking = Booking.objects.get(pk=response.data['id'])
        self.assertEqual(booking.user,self.customer)
        detail = f'{path}{booking.pk}/'
        self.assertEqual(self.client.get(path).data['count'],1)
        self.assertEqual(self.client.put(detail,{**payload,'no_of_guests':4}).status_code,200)
        self.assertEqual(self.client.patch(detail,{'name':'Ada Updated'}).status_code,200)
        self.authenticate(self.other)
        self.assertEqual(self.client.get(path).data['count'],0)
        self.assertEqual(self.client.get(detail).status_code,404)
        self.assertEqual(self.client.patch(detail,{'name':'Intruder'}).status_code,404)
        self.assertEqual(self.client.delete(detail).status_code,404)
        self.authenticate(self.staff)
        self.assertEqual(self.client.get(path).data['count'],1)
        self.authenticate(self.customer)
        self.assertEqual(self.client.delete(detail).status_code,204)
        self.assertFalse(Booking.objects.filter(pk=booking.pk).exists())

    def test_booking_invalid_data_does_not_persist(self):
        self.authenticate(self.customer)
        path = '/restaurant/booking/tables/'
        future = (timezone.now()+timedelta(days=1)).isoformat()
        for count in [0,-1,21]:
            response = self.client.post(path,{'name':'Ada','no_of_guests':count,'booking_date':future})
            self.assertEqual(response.status_code,400)
        response = self.client.post(path,{'name':'Ada','no_of_guests':2,'booking_date':(timezone.now()-timedelta(days=1)).isoformat()})
        self.assertEqual(response.status_code,400)
        self.assertEqual(Booking.objects.count(),0)

    def test_filter_order_and_aliases(self):
        Menu.objects.create(title='Soup',price='6.50',inventory=10)
        response = self.client.get('/restaurant/menu/?ordering=price')
        self.assertEqual(response.data['results'][0]['title'],'Soup')
        self.assertEqual(self.client.get('/api/menu/?search=Pasta').data['count'],1)
        self.authenticate(self.customer)
        self.assertEqual(self.client.get('/api/bookings/').status_code,200)
