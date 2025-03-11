from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tour.models import Vendor, Package, CustomUser
from tour.forms import PackageForm
from django.utils.timezone import now

# 🚀 Admin Dashboard
@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        return redirect('home')

    total_users = CustomUser.objects.filter(is_vendor=False, is_admin=False).count()
    total_vendors = Vendor.objects.count()
    pending_vendors = Vendor.objects.filter(is_approved=False).count()

    context = {
        'total_users': total_users,
        'total_vendors': total_vendors,
        'pending_vendors': pending_vendors
    }
    return render(request, 'tour/admin_dashboard.html', context)

# ✅ Approve Vendor
@login_required
def approve_vendor(request, vendor_id):
    if not request.user.is_admin:
        return redirect('home')

    vendor = get_object_or_404(Vendor, id=vendor_id)
    vendor.is_approved = True
    vendor.save()

    messages.success(request, f'Vendor "{vendor.company_name}" has been approved!')
    return redirect('vendor_list')

# ❌ Reject & Delete Vendor
@login_required
def reject_vendor(request, vendor_id):
    if not request.user.is_admin:
        return redirect('home')

    vendor = get_object_or_404(Vendor, id=vendor_id)
    user = vendor.user
    vendor.delete()
    user.delete()

    messages.error(request, f'Vendor "{vendor.company_name}" has been deleted.')
    return redirect('vendor_list')

# 🚨 Disable Vendor (Admin)
@login_required
def disable_vendor(request, vendor_id):
    if not request.user.is_admin:
        return redirect('home')

    vendor = get_object_or_404(Vendor, id=vendor_id)
    vendor.is_approved = False
    vendor.save()

    messages.warning(request, f'Vendor "{vendor.company_name}" has been disabled.')
    return redirect('vendor_list')

# 📦 List All Tour Packages
@login_required
def package_list(request):
    current_date = timezone.now().date()  # Get the current date
    
    # Filter non-expired packages (expiry_date >= current_date)
    non_expired_packages = Package.objects.filter(is_published=True, expiry_date__gte=current_date)
    
    # Filter expired packages (expiry_date < current_date)
    expired_packages = Package.objects.filter(is_published=True, expiry_date__lt=current_date)
    
    # Combine both lists: non-expired first, expired packages after
    packages = non_expired_packages | expired_packages

    return render(request, 'tour/package_list.html', {'packages': packages})


@login_required
def package_list(request):
    # Sort: Published first, then unpublished (disabled)
    packages = Package.objects.filter(expiry_date__gte=now()).order_by('-is_published')

    return render(request, 'tour/package_list.html', {'packages': packages, 'user': request.user})

# ✅ List of Vendors (Both Approved & Pending)
@login_required
def vendor_list(request):
    if not request.user.is_admin:
        return redirect('home')

    vendors = Vendor.objects.all().select_related('user')  # Fetch all vendors
    return render(request, 'tour/vendor_list.html', {'vendors': vendors})

@login_required
def admin_delete_package(request, package_id):
    if not request.user.is_admin:
        return redirect('home')

    package = get_object_or_404(Package, id=package_id)
    package.delete()

    messages.success(request, f'Package "{package.title}" has been deleted by the admin.')
    return redirect('admin_dashboard')
