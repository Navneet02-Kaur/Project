from django.db import models

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=[('individual', 'Individual'), ('organization', 'Organization')])
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'main_users'

class OffsetProject(models.Model):
    CATEGORY_CHOICES = [
        ('Tree Plantation', 'Tree Plantation'),
        ('Solar Energy', 'Solar Energy'),
        ('Waste Management', 'Waste Management')
    ]
    project_name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Tree Plantation')
    location = models.CharField(max_length=200, default='Unknown')  # Ensure location field is defined
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
