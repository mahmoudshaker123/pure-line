from django import forms

from .models import Inquiry


class InquiryForm(forms.ModelForm):
    website = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"autocomplete": "off", "tabindex": "-1", "aria-hidden": "true"}
        ),
    )

    class Meta:
        model = Inquiry
        fields = ("name", "phone", "email", "service", "location", "message")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "الاسم الكريم", "autocomplete": "name"}),
            "phone": forms.TextInput(attrs={"placeholder": "05xxxxxxxx", "inputmode": "tel", "autocomplete": "tel"}),
            "email": forms.EmailInput(attrs={"placeholder": "البريد الإلكتروني - اختياري", "autocomplete": "email"}),
            "service": forms.Select(attrs={"aria-label": "اختر الخدمة"}),
            "location": forms.TextInput(attrs={"placeholder": "المدينة أو موقع المشروع"}),
            "message": forms.Textarea(attrs={"placeholder": "حدثنا باختصار عن احتياج المشروع", "rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"].queryset = self.fields["service"].queryset.filter(is_active=True)
        self.fields["service"].empty_label = "اختر الخدمة المطلوبة"
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_website(self):
        value = self.cleaned_data.get("website", "")
        if value:
            raise forms.ValidationError("تعذر إرسال الطلب.")
        return value
