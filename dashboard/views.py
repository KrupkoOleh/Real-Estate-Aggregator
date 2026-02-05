from django.views.generic import ListView

from dashboard.models import Listening


class ListeningListView(ListView):
    model = Listening
    template_name = 'listening/main.html'
