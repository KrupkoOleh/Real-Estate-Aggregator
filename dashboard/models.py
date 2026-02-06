from django.db import models

from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin


class Listening(PKMixin):
    title = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=MAX_DIGITS,
                                decimal_places=DECIMAL_PLACES)
    link = models.CharField(max_length=256)
