from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "preview_image", "is_published"]
        labels = {
            "title": "Заголовок",
            "content": "Содержимое",
            "preview_image": "Изображение для предпросмотра",
            "is_published": "Опубликовано",
        }
