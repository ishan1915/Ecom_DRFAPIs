from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Product, Order

class EcomTests(TestCase):
    def setUp(self):
        # Create buyer and seller
        self.seller = User.objects.create_user(username='seller1', password='pass123', is_seller=True, email='seller@example.com')
        self.buyer = User.objects.create_user(username='buyer1', password='pass123', is_seller=False, email='buyer@example.com')
        
        # Create a product by seller
        self.product = Product.objects.create(
            seller=self.seller,
            name='Test Product',
            description='Test Description',
            price=100.0,
            quantity=10,
            category='Electronics'
        )

        self.client = Client()

    def test_user_registration(self):
        response = self.client.post(reverse('register_user'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass',
            'is_seller': False,
            'address': 'Test address'
        })
        self.assertEqual(response.status_code, 201)

    def test_login_buyer_redirect(self):
        response = self.client.post(reverse('login_user'), {
            'username': 'buyer1',
            'password': 'pass123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to buyer dashboard

    def test_login_seller_redirect(self):
        response = self.client.post(reverse('login_user'), {
            'username': 'seller1',
            'password': 'pass123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to seller dashboard

    def test_product_list_api(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Product', str(response.content))

    def test_create_order(self):
        self.client.login(username='buyer1', password='pass123')
        response = self.client.post(reverse('create-order'), {
            'product': self.product.id,
            'quantity': 2
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)

    def test_buyer_cannot_create_product(self):
        self.client.login(username='buyer1', password='pass123')
        response = self.client.post(reverse('product-create'), {
            'name': 'Illegal Product',
            'description': 'Should not allow',
            'price': 50,
            'quantity': 1,
            'category': 'Fake',
            'seller': self.buyer.id
        })
        self.assertNotEqual(response.status_code, 201)  # Should not allow

