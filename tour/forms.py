from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, Package, Vendor

# ✅ Normal User Registration Form
class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


# ✅ Vendor Registration Form (Requires Approval)
class VendorRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    company_name = forms.CharField(max_length=255, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True, auto_approve=False):
        user = super().save(commit=False)
        user.is_vendor = True  # ✅ Mark user as vendor
        if commit:
            user.save()
            Vendor.objects.create(
                user=user, 
                company_name=self.cleaned_data['company_name'],
                is_approved=auto_approve  # ✅ Approve instantly if needed
            )
        return user


# ✅ Package Form (For Vendors)
class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['title', 'description', 'price', 'duration', 'expiry_date', 'availability', 'image', 'is_published']
