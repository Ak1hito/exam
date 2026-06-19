from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import EventForm, ProductForm
from .models import Event, Product


class FormStatusMixin:
    """Возвращает HTTP 400 при ошибках валидации формы (требование ТЗ)."""

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response


def ping(request):
    return HttpResponse("pong")


def home(request):
    return redirect("product_list")


class ProductListView(ListView):
    model = Product
    template_name = "exam/product_list.html"
    context_object_name = "products"


class ProductCreateView(FormStatusMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "exam/form.html"
    success_url = reverse_lazy("product_list")
    extra_context = {"title": "Новый товар", "cancel_url": reverse_lazy("product_list")}


class ProductUpdateView(FormStatusMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "exam/form.html"
    success_url = reverse_lazy("product_list")
    extra_context = {"title": "Редактирование товара", "cancel_url": reverse_lazy("product_list")}


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "exam/confirm_delete.html"
    success_url = reverse_lazy("product_list")
    extra_context = {"cancel_url": reverse_lazy("product_list")}


class EventListView(ListView):
    model = Event
    template_name = "exam/event_list.html"
    context_object_name = "events"


class EventCreateView(FormStatusMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "exam/form.html"
    success_url = reverse_lazy("event_list")
    extra_context = {"title": "Новое мероприятие", "cancel_url": reverse_lazy("event_list")}


class EventUpdateView(FormStatusMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "exam/form.html"
    success_url = reverse_lazy("event_list")
    extra_context = {"title": "Редактирование мероприятия", "cancel_url": reverse_lazy("event_list")}


class EventDeleteView(DeleteView):
    model = Event
    template_name = "exam/confirm_delete.html"
    success_url = reverse_lazy("event_list")
    extra_context = {"cancel_url": reverse_lazy("event_list")}
