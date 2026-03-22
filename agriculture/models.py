from django.db import models


class FarmerRegister(models.Model):
    STATUS_CHOICES = [
        ('request', 'Request'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]
    farmer_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='request')

    class Meta:
        db_table = 'farmer_register'


class UserRegister(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=150)
    pincode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    address = models.TextField()
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'user_register'


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    farmer_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'category'


class ItemDetails(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    iditem_details = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='category_id')
    farmer = models.ForeignKey(FarmerRegister, on_delete=models.CASCADE, db_column='farmer_id')
    date_added = models.DateField()
    quantity = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    item_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'item_details'


class UserBooking(models.Model):
    STATUS_CHOICES = [
        ('ADDED', 'Added to Cart'),
        ('Paid', 'Paid'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    iduser_booking = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE, db_column='user_id')
    item = models.ForeignKey(ItemDetails, on_delete=models.CASCADE, db_column='iditem_details')
    booking_date = models.DateField()
    shipping_address = models.TextField()
    total_amount_user = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ADDED')

    class Meta:
        db_table = 'user_booking'


class Compliant(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('replied', 'Replied'),
    ]
    idcompliant = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE, db_column='user_id')
    details = models.TextField()
    date_sent = models.DateField()
    reply = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        db_table = 'compliant'
