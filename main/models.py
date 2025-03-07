from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    ROLE_CHOICES = [
        ('individual', 'Individual'),
        ('organization', 'Organization'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='individual')

    class Meta:
        db_table = 'main_users'

    def __str__(self):
        return self.email

class OffsetProject(models.Model):
    CATEGORY_CHOICES = [
        ('Tree Plantation', 'Tree Plantation'),
        ('Waste Management', 'Waste Management'),
        ('Solar Management', 'Solar Management'),
        ('Rainwater Harvesting', 'Rainwater Harvesting'),
        ('Biogas Projects', 'Biogas Projects'),
        ('E-Waste Recycling', 'E-Waste Recycling'),
        ('Plastic Waste Reduction', 'Plastic Waste Reduction'),
        ('Afforestation Projects', 'Afforestation Projects'),
        ('Community Solar Projects', 'Community Solar Projects'),
        ('Eco Brick Projects', 'Eco Brick Projects'),
    ]
    project_name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Tree Plantation')
    location = models.CharField(max_length=200, default='Unknown')
    target_amount = models.IntegerField()
    duration = models.IntegerField(null=True, blank=True)
    contact_email = models.EmailField()
    created_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'offset_project'

    def __str__(self):
        return self.project_name

class Contribution(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    project = models.ForeignKey(OffsetProject, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.CharField(max_length=100)
    created_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contribution'

    def __str__(self):
        return f"{self.name} - {self.project.project_name}"
