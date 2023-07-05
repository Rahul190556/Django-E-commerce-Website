from django.db import models
from django.contrib.auth.models import User


# Create your models here.
STATE_CHOICES = (
    ('AN', 'Andaman and Nicobar Islands'),
    ('AP', 'Andhra Pradesh'),
    ('AR', 'Arunachal Pradesh'),
    ('AS', 'Assam'),
    ('BR', 'Bihar'),
    ('CH', 'Chandigarh'),
    ('CT', 'Chhattisgarh'),
    ('DN', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('DL', 'Delhi'),
    ('GA', 'Goa'),
    ('GJ', 'Gujarat'),
    ('HR', 'Haryana'),
    ('HP', 'Himachal Pradesh'),
    ('JK', 'Jammu and Kashmir'),
    ('JH', 'Jharkhand'),
    ('KA', 'Karnataka'),
    ('KL', 'Kerala'),
    ('LA', 'Ladakh'),
    ('LD', 'Lakshadweep'),
    ('MP', 'Madhya Pradesh'),
    ('MH', 'Maharashtra'),
    ('MN', 'Manipur'),
    ('ML', 'Meghalaya'),
    ('MZ', 'Mizoram'),
    ('NL', 'Nagaland'),
    ('OD', 'Odisha'),
    ('PY', 'Puducherry'),
    ('PB', 'Punjab'),
    ('RJ', 'Rajasthan'),
    ('SK', 'Sikkim'),
    ('TN', 'Tamil Nadu'),
    ('TS', 'Telangana'),
    ('TR', 'Tripura'),
    ('UP', 'Uttar Pradesh'),
    ('UK', 'Uttarakhand'),
    ('WB', 'West Bengal')
)

class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=256)
    locality=models.CharField(max_length=256)
    city=models.CharField(max_length=54)
    zipcode=models.PositiveIntegerField(null=True)
    state=models.CharField(max_length=54,choices=STATE_CHOICES)

    def __str__(self):
        return str(self.id);

CATEGORY_CHOICES=(
    ('M','Mobile'),
    ('L',"Laptop"),
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),
)

class Product(models.Model):
    title=models.CharField(max_length=256)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField(max_length=1000)
    brand=models.CharField(max_length=50)
    category=models.CharField(max_length=2,choices=CATEGORY_CHOICES)
    product_image=models.ImageField(upload_to='productsimg')

    def __str__(self):
        return str(self.id);


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return str(self.id);

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)

class OrderPlaced(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    ordered_date=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=54,choices=STATUS_CHOICES,default='Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


# accesing tuple all values to use in search bar logic
# accesing tuples values in views.py file with query from models.py file
# category__in=[category[0] for category in CATEGORY_CHOICES if query.lower() in category[1].lower()] is the condition used for filtering.
# category__in= specifies that we want to filter by the category field of the Product model.
# [category[0] for category in CATEGORY_CHOICES if query.lower() in category[1].lower()] is a list comprehension that creates a list of category keys (category[0]) from CATEGORY_CHOICES based on certain conditions.
# for category in CATEGORY_CHOICES iterates over each category in CATEGORY_CHOICES.
# if query.lower() in category[1].lower() checks if the lowercased query exists within the lowercased category value (category[1]).
# category[0] selects the category key if the condition is met.