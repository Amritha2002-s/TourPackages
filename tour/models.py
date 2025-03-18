from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """Creates a normal user"""
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Creates a superuser with admin access"""
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)  

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser must have is_admin=True.")

        return self.create_user(username, email, password, **extra_fields)

# ✅ Custom User Model (No Django Admin Access)
class CustomUser(AbstractUser):
    is_vendor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()  # ✅ Attach custom manager

    def save(self, *args, **kwargs):
        """Ensure admin users get proper Django Admin access"""
        if self.is_admin:
            self.is_staff = True
            self.is_superuser = True  # ✅ Ensure admin is also superuser
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

# ✅ Vendor Model (Requires Admin Approval)
class Vendor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, unique=True)
    is_approved = models.BooleanField(default=False)  # 🚀 Manual approval system

    def __str__(self):
        return self.company_name

# ✅ Tour Package Model
class Package(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="packages")
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField()  # ⏳ Duration in days
    expiry_date = models.DateField()
    image = models.ImageField(upload_to='packages/', blank=True, null=True)  # 📷 Optional image
    is_published = models.BooleanField(default=False)
    availability = models.PositiveIntegerField(default=0)  # 🎟 Available slots

    class Meta:
        ordering = ['-expiry_date']  # ✅ Show latest packages first
        verbose_name = "Tour Package"
        verbose_name_plural = "Tour Packages"

    def __str__(self):
        return f"{self.title} - {self.vendor.company_name}"

# ✅ Booking Model
class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="bookings")
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)

    class Meta:
        ordering = ['-booking_date']  # ✅ Show latest bookings first

    def __str__(self):
        return f'{self.user.username} - {self.package.title}'
