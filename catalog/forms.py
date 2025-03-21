from django import forms

from .models import Product

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "photo", "category", "price"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        for word in FORBIDDEN_WORDS:
            if word.lower() in name.lower():
                raise forms.ValidationError(
                    f"Название не должно содержать слово '{word}'."
                )
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        for word in FORBIDDEN_WORDS:
            if word.lower() in description.lower():
                raise forms.ValidationError(
                    f"Описание не должно содержать слово '{word}'."
                )
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_photo(self):
        photo = self.cleaned_data.get("photo")
        if photo:
            if not (
                photo.name.endswith(".jpg")
                or photo.name.endswith(".jpeg")
                or photo.name.endswith(".png")
            ):
                raise forms.ValidationError("Файл должен быть в формате JPEG или PNG.")
            if photo.size > 5 * 1024 * 1024:  # 5 МБ
                raise forms.ValidationError("Размер файла не должен превышать 5 МБ.")
        return photo

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": f"Введите {field.label.lower()}",
                }
            )
