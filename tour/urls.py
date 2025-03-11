from django.urls import path
from . import views
from .views import admin_views, public_views, user_views, vendor_views



urlpatterns = [
    # Public Routes
    path('', public_views.home, name='home'),
    path('register/', public_views.register, name='register'),
    path('login/', public_views.user_login, name='login'),
    path('logout/', public_views.user_logout, name='logout'),

    # Dashboard
    path('dashboard/', user_views.dashboard, name='dashboard'),

    # Packages
    path('packages/', admin_views.package_list, name='package_list'),
    path('book/<int:package_id>/', vendor_views.book_package, name='book_package'),
    path('toggle-package/<int:package_id>/', vendor_views.toggle_package_status, name='toggle_package_status'),
    path('payment_success/', vendor_views.payment_success, name='payment_success'),

    # Vendor Routes
    path('vendor/dashboard/', vendor_views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/register/', vendor_views.register_vendor, name='register_vendor'),
    path('vendor/package/create/', vendor_views.create_package, name='create_package'),
    path('vendor/package/edit/<int:package_id>/', vendor_views.edit_package, name='edit_package'),
    path('vendor/package/delete/<int:package_id>/', vendor_views.delete_package, name='delete_package'),

    # Admin Routes
    path('admin-dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('vendor_list/', admin_views.vendor_list, name='vendor_list'),
    path('admin/package/delete/<int:package_id>/', admin_views.admin_delete_package, name='admin_delete_package'),
    path('approve-vendor/<int:vendor_id>/', admin_views.approve_vendor, name='approve_vendor'),
    path('reject-vendor/<int:vendor_id>/', admin_views.reject_vendor, name='reject_vendor'),
    path('disable-vendor/<int:vendor_id>/', admin_views.disable_vendor, name='disable_vendor'),  # Disable vendor
]
