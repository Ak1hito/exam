from django import forms
from django.db import models

from .models import Event, Product


DATETIME_LOCAL_FORMAT = "%Y-%m-%dT%H:%M"
DATE_LOCAL_FORMAT = "%Y-%m-%d"


def setup_form_fields(form):
    for name, field in form.fields.items():
        model_field = form._meta.model._meta.get_field(name)
        # DateTimeField проверяем раньше DateField: он является его подклассом.
        if isinstance(model_field, models.DateTimeField):
            field.input_formats = [DATETIME_LOCAL_FORMAT]
            field.widget = forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"},
                format=DATETIME_LOCAL_FORMAT,
            )
        elif isinstance(model_field, models.DateField):
            field.input_formats = [DATE_LOCAL_FORMAT]
            field.widget = forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format=DATE_LOCAL_FORMAT,
            )
        elif isinstance(model_field, models.BooleanField):
            field.widget.attrs["class"] = "form-check-input"
        else:
            field.widget.attrs["class"] = "form-control"


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "price", "sku"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        setup_form_fields(self)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "location", "event_date", "max_guests"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        setup_form_fields(self)
