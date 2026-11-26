from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):

    quantity = forms.IntegerField(
        min_value=0,
        initial=1,
        label="Available Stock"
    )

    class Meta:
        model = Product

        fields = [
            'category',
            'name',
            'description',
            'price',
            'unit'
        ]

        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'min': '0.01',
                'step': '0.01'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Do not allow new products to be assigned to disabled categories.
        self.fields['category'].queryset = Category.objects.filter(
            is_active=True
        )

    def clean_price(self):
        price = self.cleaned_data['price']

        if price <= 0:
            raise forms.ValidationError(
                "Price must be greater than zero."
            )

        return price
