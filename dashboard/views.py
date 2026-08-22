

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from .decorators import admin_required, vendor_required
from django.contrib.auth import authenticate, login
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from functools import wraps
from django.shortcuts import redirect
from .models import (
    Vendor,
    Quotation,
    Invoice,
    PurchaseOrder,
    VendorRegistration,
    VendorContact,
    VendorDocument,
)
from .forms import (
    LoginForm,
    VendorForm,
    QuotationForm,
    InvoiceForm,
    PurchaseOrderForm,
    VendorRegistrationForm,
    VendorContactForm,
    VendorDocumentForm,
)
from .decorators import admin_required, vendor_required
from django.contrib.auth import authenticate, login
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
def admin_required(view_func):
    return user_passes_test(
        lambda user: user.is_authenticated and user.is_staff,
        login_url="vendor_dashboard"
    )(view_func)

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login")

        if not request.user.is_staff:
            return redirect("vendor_dashboard")

        return view_func(request, *args, **kwargs)

    return _wrapped_view


@login_required(login_url="login")
@admin_required
def home(request):

    total_vendors = Vendor.objects.count()
    active_vendors = Vendor.objects.filter(status="Active").count()

    total_quotations = Quotation.objects.count()
    approved_quotations = Quotation.objects.filter(status="Approved").count()
    pending_quotations = Quotation.objects.filter(status="Pending").count()
    rejected_quotations = Quotation.objects.filter(status="Rejected").count()

    total_purchase_orders = PurchaseOrder.objects.count()

    total_invoices = Invoice.objects.count()
    approved_invoices = Invoice.objects.filter(status="Approved").count()
    pending_invoices = Invoice.objects.filter(status="Pending").count()
    paid_invoices = Invoice.objects.filter(status="Paid").count()

    total_amount = Invoice.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0

    recent_quotations = Quotation.objects.order_by("-id")[:5]
    recent_invoices = Invoice.objects.order_by("-id")[:5]

    context = {

        "total_vendors": total_vendors,
        "active_vendors": active_vendors,

        "total_quotations": total_quotations,
        "approved_quotations": approved_quotations,
        "pending_quotations": pending_quotations,
        "rejected_quotations": rejected_quotations,

        "total_purchase_orders": total_purchase_orders,

        "total_invoices": total_invoices,
        "approved_invoices": approved_invoices,
        "pending_invoices": pending_invoices,
        "paid_invoices": paid_invoices,

        "total_amount": total_amount,

        "recent_quotations": recent_quotations,
        "recent_invoices": recent_invoices,
    }

    return render(
        request,
        "dashboardhome/dashboard.html",
        context
    )


    return render(request, "dashboardhome/register.html")

def login_view(request):

    form = LoginForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:

                # =========================
                # CHECK VENDOR
                # =========================

                vendor = Vendor.objects.filter(
                    user=user
                ).first()

                if vendor is not None:

                    login(request, user)

                    request.session["role"] = "vendor"

                    return redirect("vendor_dashboard")


                # =========================
                # CHECK ADMIN
                # =========================

                if user.is_staff or user.is_superuser:

                    login(request, user)

                    request.session["role"] = "admin"

                    return redirect("home")


                # =========================
                # NOT AUTHORIZED
                # =========================

                return render(
                    request,
                    "dashboardhome/login.html",
                    {
                        "form": form,
                        "error": "You are not authorized to access the portal."
                    }
                )


            else:

                return render(
                    request,
                    "dashboardhome/login.html",
                    {
                        "form": form,
                        "error": "Invalid Username or Password"
                    }
                )

    return render(
        request,
        "dashboardhome/login.html",
        {
            "form": form
        }
    )

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect("login")


@login_required(login_url="login")
@admin_required
@user_passes_test(admin_required, login_url="login")
def vendor_list(request):

    search = request.GET.get("search")

    if search:
        vendors = Vendor.objects.filter(
            company_name__icontains=search
        )
    else:
        vendors = Vendor.objects.all()

    context = {
        "vendors": vendors
    }

    return render(
        request,
        "dashboardhome/vendor_list.html",
        context
    )

@login_required(login_url="login")
@admin_required
@user_passes_test(admin_required, login_url="login")
def add_vendor(request):

    if request.method == "POST":
        form = VendorForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("vendor_list")

    else:
        form = VendorForm()

    return render(
        request,
        "dashboardhome/vendor_form.html",
        {"form": form},
    )


@login_required(login_url="login")
@admin_required
@user_passes_test(admin_required, login_url="login")
def edit_vendor(request, id):

    vendor = get_object_or_404(Vendor, id=id)

    if request.method == "POST":

        form = VendorForm(request.POST, instance=vendor)

        if form.is_valid():
            form.save()
            return redirect("vendor_list")

    else:
        form = VendorForm(instance=vendor)

    return render(
        request,
        "dashboardhome/vendor_form.html",
        {
            "form": form
        }
    )

@login_required(login_url="login")
@admin_required
@user_passes_test(admin_required, login_url="login")
def delete_vendor(request, id):

    vendor = get_object_or_404(Vendor, id=id)

    vendor.delete()

    return redirect("vendor_list")

# Quotation
@login_required(login_url="login")
@admin_required
@user_passes_test(admin_required, login_url="login")
def quotation_list(request):

    quotations = Quotation.objects.all()

    context = {
        "quotations": quotations
    }

    return render(
        request,
        "dashboardhome/quotation_list.html",
        context
    )
# Quotation Form

@login_required(login_url="login")
@admin_required
@user_passes_test(admin_required, login_url="login")
def add_quotation(request):

    if request.method == "POST":

        form = QuotationForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("quotation_list")

    else:

        form = QuotationForm()

    return render(
        request,
        "dashboardhome/quotation_form.html",
        {"form": form}
    )

@login_required(login_url="login")
@admin_required
@user_passes_test(admin_required, login_url="login")
def edit_quotation(request, id):

    quotation = get_object_or_404(Quotation, id=id)

    if request.method == "POST":

        form = QuotationForm(request.POST, instance=quotation)

        if form.is_valid():

            form.save()

            return redirect("quotation_list")

    else:

        form = QuotationForm(instance=quotation)

    return render(
        request,
        "dashboardhome/quotation_form.html",
        {"form": form}
    )

@login_required(login_url="login")
@admin_required
@user_passes_test(admin_required, login_url="login")
def delete_quotation(request, id):

    quotation = get_object_or_404(Quotation, id=id)

    quotation.delete()

    return redirect("quotation_list")

@login_required(login_url="login")
@admin_required
@user_passes_test(admin_required, login_url="login")
def approve_quotation(request, id):
    quotation = get_object_or_404(Quotation, id=id)
    quotation.status = "Approved"
    quotation.save()
    return redirect("quotation_list")

@login_required(login_url="login")
@admin_required
@user_passes_test(admin_required, login_url="login")
def reject_quotation(request, id):
    quotation = get_object_or_404(Quotation, id=id)
    quotation.status = "Rejected"
    quotation.save()
    return redirect("quotation_list")


from django.db.models import Sum

@login_required(login_url="login")
@admin_required
@user_passes_test(admin_required, login_url="login")
def invoice_list(request):

    invoices = Invoice.objects.all()

    selected_invoice = None

    invoice_id = request.GET.get("invoice")

    if invoice_id:
        selected_invoice = Invoice.objects.filter(id=invoice_id).first()

    context = {
        "invoices": invoices,
        "selected_invoice": selected_invoice,
        "pending": invoices.filter(status="Pending").count(),
        "approved": invoices.filter(status="Approved").count(),
        "rejected": invoices.filter(status="Rejected").count(),
        "total_amount": invoices.aggregate(total=Sum("amount"))["total"] or 0,
    }

    return render(
        request,
        "dashboardhome/invoice_list.html",
        context,
    )
@login_required(login_url="login")
@admin_required
@user_passes_test(admin_required, login_url="login")
def add_invoice(request):

    if request.method == "POST":

        print("POST:", request.POST)
        print("FILES:", request.FILES)

        form = InvoiceForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()
            return redirect("invoice_list")
        else:
            print(form.errors)

    else:
        form = InvoiceForm()

    return render(
        request,
        "dashboardhome/invoice_form.html",
        {
            "form": form
        }
    )
@login_required(login_url="login")
@admin_required
@user_passes_test(admin_required, login_url="login")
def edit_invoice(request, id):
    invoice = get_object_or_404(Invoice, id=id)

    if request.method == "POST":
        form = InvoiceForm(request.POST, request.FILES, instance=invoice)

        if form.is_valid():
            form.save()
            return redirect("invoice_list")
    else:
        form = InvoiceForm(instance=invoice)

    return render(
        request,
        "dashboardhome/invoice_form.html",
        {
            "form": form
        }
    )
@login_required(login_url="login")
@admin_required
@user_passes_test(admin_required, login_url="login")
def delete_invoice(request, id):

    invoice = get_object_or_404(Invoice, id=id)

    invoice.delete()

    return redirect("invoice_list")

@login_required(login_url="login")
@admin_required
@user_passes_test(admin_required, login_url="login")
def approve_invoice(request, id):

    invoice = get_object_or_404(Invoice, id=id)

    invoice.status = "Approved"

    invoice.save()

    return redirect("invoice_list")
@login_required(login_url="login")
@admin_required
@user_passes_test(admin_required, login_url="login")
def reject_invoice(request, id):

    invoice = get_object_or_404(Invoice, id=id)

    invoice.status = "Rejected"

    invoice.save()

    return redirect("invoice_list")

# Vendorlogin


def vendor_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            vendor = Vendor.objects.filter(
                user=user
            ).first()

            if vendor is not None:

                login(request, user)

                request.session["role"] = "vendor"

                return redirect("vendor_dashboard")

            return render(
                request,
                "dashboardhome/vendor_login.html",
                {
                    "error": "You are not registered as an approved vendor."
                }
            )

        return render(
            request,
            "dashboardhome/vendor_login.html",
            {
                "error": "Invalid Username or Password."
            }
        )

    return render(
        request,
        "dashboardhome/vendor_login.html"
    )

@login_required(login_url="vendor_login")
@vendor_required
def vendor_dashboard(request):

    vendor = get_object_or_404(
        Vendor,
        user=request.user
    )

    return render(
        request,
        "dashboardhome/vendor_dashboard.html",
        {
            "vendor": vendor
        }
    )

@login_required(login_url="login")
@vendor_required
@user_passes_test(admin_required, login_url="login")
def vendor_quotation_list(request):

    vendor = get_object_or_404(
        Vendor,
        user=request.user
    )

    quotations = Quotation.objects.filter(
        vendor=vendor
    )

    return render(
        request,
        "dashboardhome/vendor_quotation_list.html",
        {
            "quotations": quotations
        }
    )

@login_required(login_url="login")
@admin_required
@user_passes_test(admin_required, login_url="login")
def purchase_order_list(request):

    purchase_orders = PurchaseOrder.objects.all()

    return render(
        request,
        "dashboardhome/purchase_order_list.html",
        {
            "purchase_orders": purchase_orders
        }
    )

@login_required(login_url="login")
@admin_required
@user_passes_test(admin_required, login_url="login")
def generate_purchase_order(request, quotation_id):

    quotation = get_object_or_404(
        Quotation,
        id=quotation_id
    )

    if request.method == "POST":

        form = PurchaseOrderForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("purchase_order_list")

    else:

        form = PurchaseOrderForm(
            initial={
                "vendor": quotation.vendor,
                "quotation": quotation,
                "amount": quotation.amount,
            }
        )

    return render(
        request,
        "dashboardhome/purchase_order_form.html",
        {
            "form": form
        }
    )

@login_required(login_url="login")
@admin_required
def add_purchase_order(request):

    if request.method == "POST":

        form = PurchaseOrderForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("purchase_order_list")

    else:

        form = PurchaseOrderForm()

    return render(
        request,
        "dashboardhome/purchase_order_form.html",
        {
            "form": form
        }
    )

@login_required(login_url="login")
@admin_required
@user_passes_test(admin_required, login_url="login")
def edit_purchase_order(request, id):

    purchase_order = get_object_or_404(
        PurchaseOrder,
        id=id
    )

    if request.method == "POST":

        form = PurchaseOrderForm(
            request.POST,
            instance=purchase_order
        )

        if form.is_valid():

            form.save()

            return redirect("purchase_order_list")

    else:

        form = PurchaseOrderForm(
            instance=purchase_order
        )

    return render(
        request,
        "dashboardhome/purchase_order_form.html",
        {
            "form": form
        }
    )

@login_required(login_url="login")
@admin_required
@user_passes_test(admin_required, login_url="login")
def delete_purchase_order(request, id):

    purchase_order = get_object_or_404(
        PurchaseOrder,
        id=id
    )

    purchase_order.delete()

    return redirect("purchase_order_list")

@login_required(login_url='login')
def profile(request):
    return render(request, 'dashboardhome/profile.html')


def register(request):

    print("REGISTER VIEW CALLED")

    if request.method == "POST":

        print(request.POST)

        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        is_staff=True
)

        print("USER CREATED:", user.username)

        return redirect("login")

    return render(request, "dashboardhome/register.html")

    # ==========================================
# Vendor Registration Module
# ==========================================

def company_information(request):

    if request.method == "POST":

        form = VendorRegistrationForm(request.POST)

        if form.is_valid():

            vendor = form.save()

            request.session["vendor_id"] = vendor.id

            return redirect("contact_information")

    else:

        form = VendorRegistrationForm()

    return render(
        request,
        "dashboardhome/vendor_registration/company_information.html",
        {
            "form": form
        }
    )


def contact_information(request):

    vendor_id = request.session.get("vendor_id")

    if not vendor_id:

        return redirect("company_information")

    vendor = VendorRegistration.objects.get(id=vendor_id)

    if request.method == "POST":

        form = VendorContactForm(request.POST)

        if form.is_valid():

            contact = form.save(commit=False)

            contact.vendor = vendor

            contact.save()

            return redirect("documents_review")

    else:

        form = VendorContactForm()

    return render(
        request,
        "dashboardhome/vendor_registration/contact_information.html",
        {
            "form": form
        }
    )

def documents_review(request):

    vendor_id = request.session.get("vendor_id")

    if not vendor_id:

        return redirect("company_information")

    vendor = VendorRegistration.objects.get(id=vendor_id)

    if request.method == "POST":

        form = VendorDocumentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            document = form.save(commit=False)

            document.vendor = vendor

            document.save()

            request.session.pop("vendor_id")

            return redirect("registration_success")

    else:

        form = VendorDocumentForm()

    return render(
        request,
        "dashboardhome/vendor_registration/documents_review.html",
        {
            "form": form
        }
    )


def registration_success(request):

    return render(
        request,
        "dashboardhome/vendor_registration/registration_success.html"
    )



  

@login_required(login_url="login")
@admin_required
def approve_vendor(request, id):

    registration = get_object_or_404(
        VendorRegistration,
        id=id
    )

    # Get contact information
    contact = VendorContact.objects.filter(
        vendor=registration
    ).first()

    # Contact information is required for approval
    if contact is None:
        messages.error(
            request,
            "Vendor cannot be approved because contact information is missing."
        )

        return redirect(
            "vendor_registration_detail",
            id=registration.id
        )

    # Prevent approving the same vendor twice
    if registration.status == "Approved":
        messages.warning(
            request,
            "This vendor has already been approved."
        )

        return redirect(
            "vendor_registration_detail",
            id=registration.id
        )

    # Create Vendor in existing Vendor table
    vendor = Vendor.objects.create(
        company_name=registration.company_name,
        contact_person=contact.primary_name,
        email=contact.primary_email,
        phone=contact.primary_mobile,
        gst_number=registration.gst_number,
        city=registration.city,
        address=registration.address,
        status="Active"
    )

    # Create Vendor Login User
    username = registration.company_name.replace(" ", "").lower()

    password = "Vendor@123"

    user = User.objects.create_user(
        username=username,
        email=contact.primary_email,
        password=password
    )

    # Connect User with Vendor
    vendor.user = user
    vendor.save()

    # Update registration status
    registration.status = "Approved"
    registration.save()

    messages.success(
        request,
        "Vendor approved successfully."
    )

    # Go back to Vendor Registration list
    return redirect("vendor_registration_list")


@login_required(login_url="vendor_login")
@vendor_required
def vendor_purchase_order_list(request):

    vendor = get_object_or_404(
        Vendor,
        user=request.user
    )

    purchase_orders = PurchaseOrder.objects.filter(
        vendor=vendor
    ).order_by("-created_at")

    return render(
        request,
        "dashboardhome/vendor_purchase_order_list.html",
        {
            "purchase_orders": purchase_orders
        }
    )
@login_required(login_url="vendor_login")
@vendor_required
def vendor_invoice_list(request):

    vendor = get_object_or_404(
        Vendor,
        user=request.user
    )

    invoices = Invoice.objects.filter(
        vendor=vendor
    ).order_by("-created_at")

    selected_invoice = None

    invoice_id = request.GET.get("invoice_id")

    if invoice_id:

        selected_invoice = Invoice.objects.filter(
            id=invoice_id,
            vendor=vendor
        ).first()

    context = {
        "invoices": invoices,

        "selected_invoice": selected_invoice,

        "pending": invoices.filter(
            status="Pending"
        ).count(),

        "approved": invoices.filter(
            status="Approved"
        ).count(),

        "rejected": invoices.filter(
            status="Rejected"
        ).count(),

        "total_amount": invoices.aggregate(
            total=Sum("amount")
        )["total"] or 0,
    }

    return render(
        request,
        "dashboardhome/invoice_list.html",
        context
    )

@login_required(login_url="login")
@admin_required
def vendor_registration_list(request):

    registrations = VendorRegistration.objects.all().order_by("-created_at")

    pending_count = VendorRegistration.objects.filter(
        status="Pending"
    ).count()

    approved_count = VendorRegistration.objects.filter(
        status="Approved"
    ).count()

    return render(
        request,
        "dashboardhome/vendor_registration_list.html",
        {
            "registrations": registrations,
            "pending_count": pending_count,
            "approved_count": approved_count,
        }
    )

@login_required(login_url="login")
@admin_required
def vendor_registration_detail(request, id):

    registration = get_object_or_404(
        VendorRegistration,
        id=id
    )

    contact = VendorContact.objects.filter(
        vendor=registration
    ).first()

    documents = VendorDocument.objects.filter(
        vendor=registration
    ).first()

    return render(
        request,
        "dashboardhome/vendor_registration_detail.html",
        {
            "registration": registration,
            "contact": contact,
            "documents": documents,
        }
    )

def admin_login(request):

    form = LoginForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:

                if user.is_staff or user.is_superuser:

                    login(request, user)

                    request.session["role"] = "admin"

                    return redirect("home")

                else:

                    return render(
                        request,
                        "dashboardhome/admin_login.html",
                        {
                            "form": form,
                            "error": "You are not authorized to access the Admin Portal."
                        }
                    )

            else:

                return render(
                    request,
                    "dashboardhome/admin_login.html",
                    {
                        "form": form,
                        "error": "Invalid Admin Username or Password."
                    }
                )

    return render(
        request,
        "dashboardhome/admin_login.html",
        {
            "form": form
        }
    )

@login_required(login_url="login")
@admin_required
def reject_vendor(request, id):

    registration = get_object_or_404(
        VendorRegistration,
        id=id
    )

    registration.status = "Rejected"
    registration.save()

    return redirect("vendor_registration_detail", id=registration.id)

@login_required(login_url="login")
@admin_required
def delete_vendor_registration(request, id):

    registration = get_object_or_404(
        VendorRegistration,
        id=id
    )

    registration.delete()

    return redirect("vendor_registration_list")

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
def vendor_signup(request):

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check password
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("vendor_signup")

        # Check email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("vendor_signup")

        # Create automatic username from email
        username = email.split("@")[0]

        original_username = username
        counter = 1

        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1

        # Create the user
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        # Automatically log in the new vendor
        login(request, user)

        return redirect("company_information")

    return render(request, "dashboardhome/vendor_signup.html")

@login_required(login_url="login")
def company_information(request):

    if request.method == "POST":

        form = VendorRegistrationForm(request.POST)

        if form.is_valid():

            vendor_registration = form.save(commit=False)

            # Connect logged-in vendor user
            vendor_registration.user = request.user

            vendor_registration.save()

            # Store registration ID for next steps
            request.session["vendor_id"] = vendor_registration.id

            return redirect("contact_information")

    else:

        form = VendorRegistrationForm()

    return render(
        request,
        "dashboardhome/vendor_registration/company_information.html",
        {
            "form": form
        }
    )

@login_required(login_url="login")
def dashboard_redirect(request):

    # Admin user
    if request.user.is_superuser or request.user.is_staff:
        return redirect("home")

    # Vendor user
    return redirect("vendor_dashboard")