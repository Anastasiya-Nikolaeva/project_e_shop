from django.shortcuts import render


def home(request):
    return render(request, "./catalog/home.html")


def contacts(request):
    message = None
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message_content = request.POST.get("message")

        message = "Ваше сообщение успешно отправлено!"

    return render(request, "./catalog/contacts.html", {"message": message})
