from django.urls import path

from .views import (
    ContactsView,
    HomeView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductsByCategoryView,
    ProductsListView,
    ProductUnpublishView,
    ProductUpdateView,
)

app_name = "catalog"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_edit"),
    path(
        "products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"
    ),
    path(
        "products/<int:pk>/unpublish/",
        ProductUnpublishView.as_view(),
        name="unpublish_product",
    ),
    path(
        "category/<int:category_id>/",
        ProductsByCategoryView.as_view(),
        name="products_by_category",
    ),
]
