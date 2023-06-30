from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATE_CHOICES = (
  ('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
  ('Andhra Pradesh','Andhra Pradesh'),
  ('Arunachal Pradesh','Arunachal Pradesh'),
  ('Assam','Assam'),
  ('Bihar','Bihar'),
  ('Chandigarh','Chandigarh'),
  ('Chhattisgarh','Chhattisgarh'),
  ('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
  ('Daman and Diu','Daman and Diu'),
  ('Delhi','Delhi'),
  ('Goa','Goa'),
  ('Gujarat','Gujarat'),
  ('Haryana','Haryana'),
  ('Himachal Pradesh','Himachal Pradesh'),
  ('Jammu & Kashmir','Jammu & Kashmir'),
  ('Jharkhand','Jharkhand'),
  ('Karnataka','Karnataka'),
  ('Kerala','Kerala'),
  ('Lakshadweep','Lakshadweep'),
  ('Madhya Pradesh','Madhya Pradesh'),
  ('Maharashtra','Maharashtra'),
  ('Manipur','Manipur'),
  ('Meghalaya','Meghalaya'),
  ('Mizoram','Mizoram'),
  ('Nagaland','Nagaland'),
  ('Odisha','Odisha'),
  ('Puducherry','Puducherry'),
  ('Punjab','Punjab'),
  ('Rajasthan','Rajasthan'),
  ('Sikkim','Sikkim'),
  ('Tamil Nadu','Tamil Nadu'),
  ('Telangana','Telangana'),
  ('Tripura','Tripura'),
  ('Uttarakhand','Uttarakhand'),
  ('Uttar Pradesh','Uttar Pradesh'),
  ('West Bengal','West Bengal'),
)
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    mobile = models.IntegerField(null=True)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=8)
    state = models.CharField(choices=STATE_CHOICES, max_length=50)
    profile_image = models.ImageField(upload_to='profile_images/',null=True)
    def __str__(self):
     # return self.user.username
     return str(self.id)
    
    @property
    def address(self):
      add1=self.locality
      add2=self.city
      add3=self.state
      add4=self.zipcode
      return f'{add1} {add2} {add3} {add4}'

CHOICES= (
 ('MOBILE', 'Mobile'),
 ('ELECTRONIC', 'electronic'),
 ('FASHION', 'fashion'),
 ('APPLIANCE', 'appliance'),
)
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField()
    product_image = models.ImageField(upload_to='product_images/')
    category = models.CharField(choices=CHOICES, max_length=50)

    def __str__(self):
        return str(self.name)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
      return f"{self.product} - {self.quantity}"
    @property
    def count(self):
      return self.len(set(product.id))

    @property
    def total(self):
      return self.quantity * self.product.price


STATUS_CHOICES = (
  ('Accepted','Accepted'),
  ('Packed','Packed'),
  ('On The Way','On The Way'),
  ('Delivered','Delivered'),
  ('Cancel','Cancel')
)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')

     # Below Property will be used by orders.html page to show total cost
    def __str__(self):
        return self.product.name

    @property
    def total(self):
      return self.quantity * self.product.price
