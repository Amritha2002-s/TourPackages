from django.shortcuts import render, get_object_or_404
from tour.models import Booking
from django.contrib.auth.decorators import login_required

# 📋 User Dashboard (View Bookings)
@login_required
def dashboard(request):
    bookings = Booking.objects.filter(user=request.user).select_related('package')  
    return render(request, 'tour/dashboard.html', {'bookings': bookings})
