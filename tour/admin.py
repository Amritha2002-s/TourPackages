from django.contrib import admin
from .models import Vendor, Package, Booking

admin.site.register(Vendor)
admin.site.register(Package)
admin.site.register(Booking)
