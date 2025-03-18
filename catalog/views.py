from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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

    def get_queryset(self):
        return Product.objects.order_by('created_at')


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        obj = super().get_object()
        if obj is None:
            raise Http404("Продукт не найден")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit'] = self.request.user.has_perm('catalog.change_product')
        context['can_delete'] = self.request.user.has_perm('catalog.delete_product')
        context['can_unpublish'] = self.request.user.has_perm('catalog.can_unpublish_product')
        context['can_add'] = self.request.user.has_perm('catalog.add_product')
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy('catalog:products_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy('catalog:products_list')
    permission_required = 'catalog.change_product'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user and not request.user.has_perm('catalog.change_product'):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)  # Вывод ошибок в консоль
        return super().form_invalid(form)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy('catalog:products_list')
    permission_required = 'catalog.delete_product'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user and not request.user.has_perm('catalog.delete_product'):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return render(self.request, 'catalog/no_permission.html', status=403)


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save()
        return redirect('catalog:products_list')

    def handle_no_permission(self):
        return render(self.request, 'catalog/no_permission.html', status=403)
