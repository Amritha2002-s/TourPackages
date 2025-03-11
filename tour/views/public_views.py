from django.shortcuts import render, redirect
from tour.forms import UserRegisterForm, VendorRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
from tour.models import Vendor

# 🏡✨ Home Page
def home(request):
    return render(request, 'tour/home.html')


# 🆕👤 User Registration
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # ✅ Log in the user after successful registration
            return redirect('package_list')
    else:
        form = UserRegisterForm()

    return render(request, 'tour/register.html', {'form': form})


# 🔑🔓 User Login
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)  # ✅ Ensure `request` is passed
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)  # 🔍 Authenticate user

            if user is not None:
                # 🚨 Prevent unapproved vendors from logging in
                if hasattr(user, 'vendor') and not user.vendor.is_approved:
                    messages.error(request, "⚠️ Your vendor account is pending approval.")
                    return redirect('login')

                login(request, user)  # ✅ Log the user in

                # 🔄 Handle Redirects Based on Role
                if user.is_superuser:  # ✅ Use `is_superuser` instead of `is_admin`
                    return redirect(reverse('admin_dashboard'))
                elif hasattr(user, 'vendor'):  # ✅ Check if user is a vendor safely
                    return redirect(reverse('vendor_dashboard'))
                else:
                    return redirect(reverse('package_list'))

    else:
        form = AuthenticationForm()

    return render(request, 'tour/login.html', {'form': form})


# 🚪👋 User Logout
def user_logout(request):
    logout(request)
    messages.success(request, "✅ You have been logged out successfully!")  # ✨ Friendly feedback
    return redirect('home')  # 🔄 Redirect to home page 
