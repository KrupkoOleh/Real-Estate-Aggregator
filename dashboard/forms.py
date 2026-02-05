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
