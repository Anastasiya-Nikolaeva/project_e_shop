from django.urls import path

from .views import ContactsView, HomeView, ProductDetailView, ProductsListView

app_name = "catalog"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]
