from django.db import models


from django.contrib.auth.models import User

class Vendor(models.Model):
    company_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    gst_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    address = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=[
            ("Active", "Active"),
            ("Inactive", "Inactive"),
        ],
        default="Active"
    )

    address = models.TextField()

    def __str__(self):
        return self.company_name


class Quotation(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE
    )

    quotation_number = models.CharField(
        max_length=100,
        unique=True
    )

    requirement = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    quotation_date = models.DateField()

    valid_till = models.DateField()

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.quotation_number
    

class Invoice(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Paid", "Paid"),
    ]

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE
    )

    invoice_number = models.CharField(
        max_length=100,
        unique=True
    )

    invoice_date = models.DateField()

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    invoice_file = models.FileField(
        upload_to="invoices/"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.invoice_number
    

class PurchaseOrder(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Issued", "Issued"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE
    )

    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.CASCADE
    )

    po_number = models.CharField(
        max_length=100,
        unique=True
    )

    po_date = models.DateField()

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Issued"
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.po_number

    