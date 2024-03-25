from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)

    def update_password(self, new_password):
        self.user.set_password(new_password)
        self.user.save()
        update_session_auth_hash(self.user)  # Pass the 'user' argument

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/', null = True, blank= True)  # Assumes you have an 'upload_to' directory in your MEDIA_ROOT
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    description = models.CharField(max_length = 300)

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user_profile.user.username}'s Cart"
    

class Address(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='addresses')
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user_profile.user.username}'s Address"

class Purchase(models.Model):
    order_id=models.TextField()
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='PurchaseItem')
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0)
    

    def __str__(self):
        return f"{self.user_profile.user.username}'s Purchase"

class PurchaseItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} in {self.purchase.user_profile.user.username}'s Purchase"