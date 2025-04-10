from django.contrib.auth.models import AbstractUser , BaseUserManager
from django.db import models
import uuid

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-increment ID
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True 


class Role(BaseModel):
    name = models.CharField(max_length=50, unique=True)  # Example: Admin, User, Manager
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'roles'  # Custom table name

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, first_name, last_name, password=None, role_id=None):
        if not phone_number:
            raise ValueError("Phone number is required")
        if not first_name or not last_name:
            raise ValueError("First name and last name are required")
        if not role_id:
            raise ValueError("Role is required")  # Ensure role is provided
        
        user = self.model(phone_number=phone_number, first_name=first_name, last_name=last_name, role_id=role_id)
        user.set_password(password)  # Hash the password before saving
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    email = None  # Remove email field
    username = None  # Remove username field
    is_superuser = None  # Remove superuser field
    is_staff = None  # Remove staff field
    is_active = None  # Remove active field
    date_joined = None
    id = models.AutoField(primary_key=True)  
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=False)  # Phone number must be unique
    role_id = models.IntegerField(default=2)  # Role management
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    is_active = models.BooleanField(default=True) 

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'  # Use phone number for login
    REQUIRED_FIELDS = []  # Remove email from required fields

    class Meta:
        db_table = 'users'  # Keep the table name as 'users'

    def __str__(self):
        return self.phone_number

