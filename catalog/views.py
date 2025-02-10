from django.shortcuts import render
from catalog.models import Product


def home(request):
    # Получаем последние 5 созданных продуктов
    latest_products = Product.objects.order_by('-created_at')[:5]

    # Выводим их в консоль
    for product in latest_products:
        print(product.name)  # Выводим имя продукта в консоль

    return render(request, "./catalog/home.html", {"latest_products": latest_products})


def contacts(request):
    message = None
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message_content = request.POST.get("message")

        message = "Ваше сообщение успешно отправлено!"

    return render(request, "./catalog/contacts.html", {"message": message})
