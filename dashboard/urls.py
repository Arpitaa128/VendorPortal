from django.urls import path
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("home/", views.home, name="home"),
    # path("base/", views.base, name="base"),
    path("logout/", views.logout_view, name="logout"),
    path("vendors/", views.vendor_list, name="vendor_list"),
    path("vendors/add/", views.add_vendor, name="add_vendor"),
    path("vendors/edit/<int:id>/", views.edit_vendor, name="edit_vendor"),
    path("vendors/delete/<int:id>/", views.delete_vendor, name="delete_vendor"),
    path("quotations/",views.quotation_list,name="quotation_list"),
    path("quotations/add/",views.add_quotation,name="add_quotation"),
    path("quotations/edit/<int:id>/", views.edit_quotation, name="edit_quotation"),
    path("quotations/delete/<int:id>/",views.delete_quotation,name="delete_quotation"),
    path("quotations/approve/<int:id>/",views.approve_quotation,name="approve_quotation"),
    path("quotations/reject/<int:id>/",views.reject_quotation,name="reject_quotation"),
    path("invoices/",views.invoice_list,name="invoice_list"),
    path("invoices/add/",views.add_invoice,name="add_invoice"),
    path("invoices/edit/<int:id>/",views.edit_invoice,name="edit_invoice"),
path("invoices/delete/<int:id>/",views.delete_invoice,name="delete_invoice"),
path("invoice/approve/<int:id>/",views.approve_invoice,name="approve_invoice",),
path("invoice/reject/<int:id>/",views.reject_invoice,name="reject_invoice",),
path( "vendor/login/",views.vendor_login,  name="vendor_login"),
path("vendor/dashboard/",views.vendor_dashboard,name="vendor_dashboard"),
path("vendor/quotations/",views.vendor_quotation_list,name="vendor_quotation_list"),
path("purchase-orders/",views.purchase_order_list,name="purchase_order_list"),
path("purchase-orders/add/",views.add_purchase_order,name="add_purchase_order"),
path("purchase-orders/edit/<int:id>/",views.edit_purchase_order,name="edit_purchase_order"),
path("purchase-orders/delete/<int:id>/",views.delete_purchase_order,name="delete_purchase_order"),
path("purchase-orders/create/<int:quotation_id>/",views.generate_purchase_order,name="generate_purchase_order"),
path('profile/', views.profile, name='profile'),
path('register/', views.register, name='register'),

]

