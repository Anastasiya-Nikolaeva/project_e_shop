from django.http import Http404
from django.shortcuts import render
from catalog.models import Product


def home(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    products = Product.objects.all()

    return render(request, "catalog/home.html", {
        "latest_products": latest_products,
        "products": products,
    })


def contacts(request):
    message = None
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message_content = request.POST.get("message")

        message = "Ваше сообщение успешно отправлено!"

    return render(request, "./catalog/contacts.html", {"message": message})


def products_list(request,):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'catalog/products_list.html', context)


def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404("Продукт не найден")
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context)
