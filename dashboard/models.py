from django.db import models


from django.contrib.auth.models import User

class Vendor(models.Model):
    user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)
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

    # ============================
# Vendor Registration Models
# ============================

class VendorRegistration(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    company_name = models.CharField(max_length=200)
    legal_name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100)
    gst_number = models.CharField(max_length=20)
    pan_number = models.CharField(max_length=20)

    establishment_year = models.PositiveIntegerField()

    industry = models.CharField(max_length=100)
    products_services = models.TextField()

    annual_turnover = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    address = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


class VendorContact(models.Model):

    vendor = models.OneToOneField(
        VendorRegistration,
        on_delete=models.CASCADE
    )

    primary_name = models.CharField(max_length=100)
    primary_designation = models.CharField(max_length=100)
    primary_email = models.EmailField()
    primary_mobile = models.CharField(max_length=15)
    primary_phone = models.CharField(
        max_length=15,
        blank=True
    )

    secondary_name = models.CharField(
        max_length=100,
        blank=True
    )

    secondary_designation = models.CharField(
        max_length=100,
        blank=True
    )

    secondary_email = models.EmailField(
        blank=True
    )

    secondary_mobile = models.CharField(
        max_length=15,
        blank=True
    )

    secondary_phone = models.CharField(
        max_length=15,
        blank=True
    )

    def __str__(self):
        return self.primary_name


class VendorDocument(models.Model):

    vendor = models.OneToOneField(
        VendorRegistration,
        on_delete=models.CASCADE
    )

    registration_certificate = models.FileField(
        upload_to="vendor_documents/"
    )

    gst_certificate = models.FileField(
        upload_to="vendor_documents/"
    )

    pan_document = models.FileField(
        upload_to="vendor_documents/"
    )

    bank_document = models.FileField(
        upload_to="vendor_documents/"
    )

    company_logo = models.ImageField(
        upload_to="vendor_documents/",
        blank=True,
        null=True
    )

    other_document = models.FileField(
        upload_to="vendor_documents/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.vendor.company_name

    