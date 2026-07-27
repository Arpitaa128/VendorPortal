from django.contrib import admin

from .models import Vendor, Quotation, Invoice, PurchaseOrder


admin.site.register(Vendor)
admin.site.register(Quotation)
admin.site.register(Invoice)
admin.site.register(PurchaseOrder)