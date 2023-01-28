from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator





#work for profile value submit
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




STATE_CHOICES = (
    ('Dhaka','Dhaka'),
    ('Mymensingh','Mymensingh'),
    ('Chitaguang','Chitaguang'),
    ('Barishal','Barishal'),
    ('Commila','Commila'),
    ('Sylhet','Sylhet'),
    ('Coxs Bazer','Coxs Bazer'),
    ('Tangail','Tangail')
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    
    #new colum add
    # id = models.ForeignKey(User, on_delete=models.CASCADE)

    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)
    
    def __str__(self):
        return str(self.id)
    

CATEGORY_CHOICES = (
    
    ('F', 'Fashion'),
    ('G', 'Grocery'),
    ('LA', 'Laptop & Accessory'),
    ('MA', 'Mobile & Accessory'),
    ('MP', 'Mobile Phone'),
    ('OT', 'Others'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='producting')
    
    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str(self):
        return str(self.id)
    
    @property
    def total_cost(self):
      return self.quantity * self.product.discounted_price
    
# def __str__(self):
#     return str(self.id)

STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel')
)

    



#------------------------------



GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female')
    # ('Other', 'Other')
)

MARITAL_CHOICES = (
    ('Married', 'Married'),
    ('Single', 'Single'),
    ('Divorced', 'Divorced')
    # ('Widowed', 'Widowed'),
    # ('Other', 'Other')
)

INTEREST_CHOICES = (
    ('Fashion', 'Fashion'),
    ('Grocery', 'Grocery'),
    ('Laptop & Accessory', 'Laptop & Accessory'),
    ('Mobile & Accessory', 'Mobile & Accessory'),
    ('Mobile Phone', 'Mobile Phone'),
    ('Others', 'Others')
)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=50, blank=True)
    age = models.IntegerField()
    location = models.CharField(max_length=50, blank=True)
    phone_num = models.IntegerField()
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default='Male')
    marital = models.CharField(max_length=50, choices=MARITAL_CHOICES, default='Single')
    interest = models.CharField(max_length=50, choices=INTEREST_CHOICES, default='Fashion')
    

    def __str__(self):
        return str(self.id)






#rahib query start from here-
class DataTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username








class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    #new one for userprofileid.
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # ordered_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateField(auto_now_add=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
