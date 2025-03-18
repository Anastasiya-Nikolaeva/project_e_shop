from django.urls import path

from .views import (
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostUpdateView,
    PublishedPostListView,
    UnpublishedPostListView,
)

app_name = "blog"

urlpatterns = [
    path("", PublishedPostListView.as_view(), name="base"),
    path(
        "posts/published/", PublishedPostListView.as_view(), name="published_post_list"
    ),
    path(
        "posts/unpublished/",
        UnpublishedPostListView.as_view(),
        name="unpublished_post_list",
    ),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/new/", PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/edit/", PostUpdateView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("posts/update/<int:pk>/", PostUpdateView.as_view(), name="post_update"),
]
