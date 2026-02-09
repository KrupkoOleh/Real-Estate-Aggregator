import re
from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django_ckeditor_5.widgets import CKEditor5Widget

from dashboard.models import Listening, Image


class ListeningForm(forms.ModelForm):
    image_urls = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                     'placeholder': 'Write each image url '
                                                    'by new row'}),
        required=False,
        label="Image (URL)"
    )

    class Meta:
        model = Listening
        fields = ['title', 'price', 'link', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Назва'}),
            'price': forms.NumberInput(attrs={'class': 'form-control',
                                              'placeholder': 'Ціна'}),
            'link': forms.URLInput(attrs={'class': 'form-control',
                                          'placeholder': 'Посилання'}),
            'description': CKEditor5Widget(config_name='extends'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            images = self.instance.images.all()
            self.fields['image_urls'].initial = '\n'.join([img.image_url
                                                           for img in images])

    def clean_title(self):
        title = self.cleaned_data['title']
        qs = Listening.objects.filter(title=title)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError('Title already exists')
        return title

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Price cannot be negative')
        return price

    def clean_link(self):
        link = self.cleaned_data['link']
        qs = Listening.objects.filter(link=link)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError('Link already exists')
        return link

    def _get_urls_from_text(self, text):
        if not text:
            return []

        return [url.strip()
                for url in re.split(r'[,\s\n]+', text)
                if url.strip()]

    def clean_image_urls(self):
        image_urls_text = self.cleaned_data.get('image_urls', '')

        if not image_urls_text:
            return image_urls_text

        urls = self._get_urls_from_text(image_urls_text)
        validator = URLValidator()

        for url in urls:
            try:
                validator(url)
            except ValidationError:
                raise forms.ValidationError(f'Incorrect URL: {url}')

        return image_urls_text

    def save(self, commit=True):
        listening = super().save(commit=commit)

        image_urls_text = self.cleaned_data.get('image_urls', '')

        if self.instance.pk:
            self.instance.images.all().delete()

        if image_urls_text:
            urls = self._get_urls_from_text(image_urls_text)
            for url in urls:
                Image.objects.create(listening=listening, image_url=url)

        return listening


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image_url']
        widgets = {
            'image_url': forms.URLInput(attrs={'class': 'form-control',
                                               'placeholder': 'Image URL'}),
        }
