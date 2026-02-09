from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin


class Listening(PKMixin):
    title = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=MAX_DIGITS,
                                decimal_places=DECIMAL_PLACES)
    link = models.CharField(max_length=256)
    description = CKEditor5Field('Text',
                                 config_name='extends',
                                 null=True,
                                 blank=True)

    def __str__(self):
        return self.title


class Image(PKMixin):
    image_url = models.URLField(max_length=500)
    listening = models.ForeignKey(Listening,
                                  on_delete=models.CASCADE,
                                  related_name='images')

    def __str__(self):
        return self.listening.title
