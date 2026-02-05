from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from dashboard.forms import ListeningForm
from dashboard.models import Listening


class ListeningListView(ListView):
    model = Listening
    template_name = 'listening/main.html'


def create_listening_popup(request):
    form = ListeningForm()
    return render(request, 'parts/listening/modal-create.html', {'form': form})


class ListeningCreateView(CreateView):
    model = Listening
    form_class = ListeningForm
    template_name = 'parts/listening/modal-create.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse(status=204, headers={'HX-Refresh': 'true'})
