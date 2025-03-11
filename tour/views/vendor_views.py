from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
import razorpay
from tour.models import Booking, Vendor, Package
from tour.forms import PackageForm, VendorRegisterForm
from tour_management import settings
from django.db.models import F

# 🏪✨ Vendor Dashboard - Manage Your Packages & Bookings
@login_required
def vendor_dashboard(request):
    if not request.user.is_vendor:
        return redirect('package_list')

    vendor = get_object_or_404(Vendor, user=request.user)
    
    if not vendor.is_approved:
        return render(request, 'tour/vendor_pending.html')

    # 📦 Fetch packages created by the logged-in vendor
    packages = Package.objects.filter(vendor=vendor)

    # 📋 Fetch bookings related to vendor's packages
    bookings = Booking.objects.filter(package__vendor=vendor).select_related('user', 'package')

    return render(request, 'tour/vendor_dashboard.html', {
        'packages': packages,
        'bookings': bookings
    })


# ➕✨ Create a New Package
@login_required
def create_package(request):
    if not request.user.is_vendor:
        return redirect('package_list')

    vendor = get_object_or_404(Vendor, user=request.user)
    
    if request.method == "POST":
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            package = form.save(commit=False)
            package.vendor = vendor
            package.save()
            messages.success(request, "🎉 Package created successfully!")
            return redirect('vendor_dashboard')
    else:
        form = PackageForm()

    return render(request, 'tour/create_package.html', {'form': form})


# ✏️🛠 Edit Package Details
@login_required
def edit_package(request, package_id):
    package = get_object_or_404(Package, id=package_id, vendor__user=request.user)
    
    if request.method == "POST":
        form = PackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Package updated successfully!")
            return redirect('vendor_dashboard')
    else:
        form = PackageForm(instance=package)

    return render(request, 'tour/edit_package.html', {'form': form})


# ❌🚀 Delete a Package
@login_required
def delete_package(request, package_id):
    package = get_object_or_404(Package, id=package_id, vendor__user=request.user)
    package.delete()
    messages.success(request, "🗑️ Package deleted successfully!")
    return redirect('vendor_dashboard')


# 🎟️💰 Book a Tour Package & Handle Payment
@login_required
def book_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    # ⚠️ Check if package is available
    if package.availability <= 0:
        messages.error(request, "😢 Sorry, this package is fully booked!")
        return redirect('package_list')

    # 🏦 Create a Razorpay Order
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    order_data = {
        "amount": int(package.price * 100),  # Razorpay works in paise (₹1 = 100 paise)
        "currency": "INR",
        "payment_capture": 1  # Auto capture payment
    }
    order = client.order.create(order_data)

    # 📝 Save booking with payment_status=False (pending)
    booking = Booking.objects.create(user=request.user, package=package)

    # 🔽 Reduce package availability atomically
    Package.objects.filter(id=package_id, availability__gt=0).update(availability=F('availability') - 1)

    context = {
        'package': package,
        'razorpay_order_id': order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount': package.price,
        'booking': booking
    }

    return render(request, 'tour/book_package.html', context)


# 🔄📢 Toggle Package Visibility (Admin Only)
@staff_member_required
def toggle_package_status(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    package.is_published = not package.is_published  # 🔄 Toggle status
    package.save()
    return redirect('package_list')


# ✅🎉 Payment Success Handler
@login_required
def payment_success(request):
    package_id = request.GET.get('package_id')
    package = get_object_or_404(Package, id=package_id)

    # 🔍 Find the existing pending booking
    booking = Booking.objects.filter(user=request.user, package=package, payment_status=False).first()

    if booking:
        # ✅ Mark it as paid instead of creating a new one
        booking.payment_status = True
        booking.save()
    else:
        # 🛑 If no pending booking is found, create a new one (Failsafe)
        booking = Booking.objects.create(user=request.user, package=package, payment_status=True)

    return render(request, 'tour/payment_success.html', {'package': package})



# 🆕📩 Vendor Registration (Pending Admin Approval)
def register_vendor(request):
    if request.method == 'POST':
        form = VendorRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_vendor = True
            user.save()
            Vendor.objects.create(user=user, company_name=form.cleaned_data['company_name'])
            messages.info(request, "🕒 Your account is pending approval. Please wait for admin approval.")
            return redirect('login')  # Don't log in until approved
    else:
        form = VendorRegisterForm()

    return render(request, 'tour/register_vendor.html', {'form': form})
