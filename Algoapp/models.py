from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2)
    price_quarterly = models.DecimalField(max_digits=10, decimal_places=2)
    price_yearly = models.DecimalField(max_digits=10, decimal_places=2)

    desc_monthly = models.CharField(max_length=1000, default="Description")
    desc_quarterly = models.CharField(max_length=1000, default="Description")
    desc_yearly = models.CharField(max_length=1000, default="Description")

    def __str__(self):
        return self.name

class UserMembership(models.Model):
    SUBSCRIPTION_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership_plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE)
    expiration_date = models.DateField()
    subscription_period = models.CharField(max_length=10, choices=SUBSCRIPTION_CHOICES)

    def __str__(self):
        return f"{self.user.username}'s Membership ({self.subscription_period})"



def upload_to(instance, filename):
    return filename.format(filename=filename)

class Blog(models.Model):
    image = models.ImageField(upload_to=upload_to)
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateField('date published')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

class BusinessDetails(models.Model):
    image = models.ImageField(upload_to=upload_to)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title
    
class Newsletter_users(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email


way_to_contacts = [
    ("Phone", "Phone"),
    ("Email", "Email"),
]

class our_clients(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField()
    phone_number = models.CharField(max_length=12)
    whatsapp_number = models.CharField(max_length=12)
    question = models.TextField()
    way_to_contact = models.CharField(max_length=100, choices=way_to_contacts)

    def __str__(self):
        return self.first_name
    

class free_triel_users(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)