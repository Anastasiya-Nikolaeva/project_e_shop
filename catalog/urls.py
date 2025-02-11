from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.home, name="home"),
    path("contacts/", views.contacts, name="contacts"),
    path('products_list/', views.products_list, name='products_list'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail')
]
