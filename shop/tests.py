from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Category, Product, Basket


class CategoryModelTest(TestCase):
    def test_category_str_method(self):
        category = Category.objects.create(name='TestCategory', slug='test-category')
        self.assertEqual(str(category), 'TestCategory')


class ProductModelTest(TestCase):
    def test_product_str_method(self):
        category = Category.objects.create(name='TestCategory', slug='test-category')
        product = Product.objects.create(category=category, name='TestProduct', slug='test-product', price=10.0)
        self.assertEqual(str(product), 'TestProduct')


class ProductsOfCategoryViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='TestCategory', slug='test-category')
        image = Image.new('RGB', (100, 100))
        tmp_file = io.BytesIO()
        image.save(tmp_file, format='JPEG')
        tmp_file.seek(0)
        self.product = Product.objects.create(
            category=self.category,
            name='TestProduct',
            slug='test-product',
            price=10.0,
            image=SimpleUploadedFile("test_product.jpg", tmp_file.read()),
        )
        self.url = reverse('shop:products_of_category', args=['test-category'])

    def test_products_of_category_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/products_of_category.html')

        products = response.context['products']
        product = products[0]

        self.assertTrue(product.image)
        self.assertTrue(product.image.url)


class BasketPageViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.category = Category.objects.create(name='TestCategory', slug='test-category')
        self.product = Product.objects.create(category=self.category, name='TestProduct', slug='test-product',
                                              price=10.0)
        self.basket = Basket.objects.create(user=self.user, product=self.product, quantity=2)
        self.url = reverse('shop:basket_page')

    def test_basket_page_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/baskets.html')
