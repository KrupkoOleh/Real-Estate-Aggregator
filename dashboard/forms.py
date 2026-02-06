from django import forms

from dashboard.models import Listening


class ListeningForm(forms.ModelForm):
    class Meta:
        model = Listening
        fields = ['title', 'price', 'link']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Назва'}),
            'price': forms.NumberInput(attrs={'class': 'form-control',
                                              'placeholder': 'Ціна'}),
            'link': forms.URLInput(attrs={'class': 'form-control',
                                          'placeholder': 'Посилання'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if Listening.objects.filter(title=title).exists():
            raise forms.ValidationError('Title already exists')
        return title

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Price cannot be negative')
        return price

    def clean_link(self):
        link = self.cleaned_data['link']
        if Listening.objects.filter(link=link).exists():
            raise forms.ValidationError('Link already exists')
        return link
