from django.http import Http404
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from catalog.models import Product


class HomeView(TemplateView):
    template_name = "catalog/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_products"] = Product.objects.order_by("-created_at")[:5]
        context["products"] = Product.objects.all()
        return context


class ContactsView(View):
    template_name = "./catalog/contacts.html"

    def get(self, request):
        return render(request, self.template_name, {"message": None})

    def post(self, request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message_content = request.POST.get("message")

        message = "Ваше сообщение успешно отправлено!"
        return render(request, self.template_name, {"message": message})


class ProductsListView(ListView):
    model = Product
    template_name = "catalog/products_list.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj is None:
            raise Http404("Продукт не найден")
        return obj
