from django import forms
from .models import Vendor
from .models import Vendor, Quotation, Invoice, PurchaseOrder
from django import forms
from captcha.fields import CaptchaField

class VendorForm(forms.ModelForm):

    class Meta:
        model = Vendor

        fields = [
    "company_name",
    "contact_person",
    "email",
    "phone",
    "gst_number",
    "city",
    "status",
    "address",
]

        widgets = {

            "company_name": forms.TextInput(attrs={
                "style":"width:95%;height:42px;padding-left:10px;border:1px solid #CCCCCC;border-radius:6px;font-size:14px;",
                "placeholder":"Enter Company Name"
            }),

            "contact_person": forms.TextInput(attrs={
                "style":"width:95%;height:42px;padding-left:10px;border:1px solid #CCCCCC;border-radius:6px;font-size:14px;",
                "placeholder":"Enter Contact Person"
            }),

            "email": forms.EmailInput(attrs={
                "style":"width:95%;height:42px;padding-left:10px;border:1px solid #CCCCCC;border-radius:6px;font-size:14px;",
                "placeholder":"Enter Email Address"
            }),

            "phone": forms.TextInput(attrs={
                "style":"width:95%;height:42px;padding-left:10px;border:1px solid #CCCCCC;border-radius:6px;font-size:14px;",
                "placeholder":"Enter Phone Number"
            }),

            "address": forms.Textarea(attrs={
                "rows":4,
                "style":"width:98%;padding:10px;border:1px solid #CCCCCC;border-radius:6px;font-size:14px;",
                "placeholder":"Enter Address"
            }),

            
        }
        
# Quotation

class QuotationForm(forms.ModelForm):

    class Meta:
        model = Quotation

        fields = [
            "vendor",
            "quotation_number",
            "requirement",
            "description",
            "quotation_date",
            "valid_till",
            "amount",
            "status",
            "remarks",
        ]

        widgets = {

            "vendor": forms.Select(attrs={
                "style":"width:98%;height:42px;border:1px solid #CCCCCC;border-radius:6px;padding-left:10px;"
            }),

            "quotation_number": forms.TextInput(attrs={
                "style":"width:95%;height:42px;border:1px solid #CCCCCC;border-radius:6px;padding-left:10px;",
                "placeholder":"Enter Quotation Number"
            }),

            "requirement": forms.TextInput(attrs={
                "style":"width:95%;height:42px;border:1px solid #CCCCCC;border-radius:6px;padding-left:10px;",
                "placeholder":"Enter Requirement"
            }),

            "description": forms.Textarea(attrs={
                "rows":4,
                "style":"width:98%;border:1px solid #CCCCCC;border-radius:6px;padding:10px;",
                "placeholder":"Enter Description"
            }),

            "quotation_date": forms.DateInput(attrs={
                "type":"date",
                "style":"width:95%;height:42px;border:1px solid #CCCCCC;border-radius:6px;padding-left:10px;"
            }),

            "valid_till": forms.DateInput(attrs={
                "type":"date",
                "style":"width:95%;height:42px;border:1px solid #CCCCCC;border-radius:6px;padding-left:10px;"
            }),

            "amount": forms.NumberInput(attrs={
                "style":"width:95%;height:42px;border:1px solid #CCCCCC;border-radius:6px;padding-left:10px;",
                "placeholder":"Enter Amount"
            }),

            "status": forms.Select(attrs={
                "style":"width:98%;height:42px;border:1px solid #CCCCCC;border-radius:6px;padding-left:10px;"
            }),

            "remarks": forms.Textarea(attrs={
                "rows":4,
                "style":"width:98%;border:1px solid #CCCCCC;border-radius:6px;padding:10px;",
                "placeholder":"Enter Remarks"
            }),

        }
class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice

        fields = [
            "vendor",
            "invoice_number",
            "invoice_date",
            "amount",
            "invoice_file",
            "status",
            "remarks",
        ]     
class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder

        fields = [
            "vendor",
            "quotation",
            "po_number",
            "po_date",
            "amount",
            "status",
            "remarks",
        ]

        widgets = {
            "po_date": forms.DateInput(attrs={"type": "date"}),
        }  

        from django import forms


class LoginForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "name": "username",
            "placeholder": "Enter Username",
            "style": "width:95%;height:40px;border:none;outline:none;font-size:14px;"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "name": "password",
            "id": "password",
            "placeholder": "Enter Password",
            "style": "width:95%;height:40px;border:none;outline:none;font-size:14px;"
        })
    )
   