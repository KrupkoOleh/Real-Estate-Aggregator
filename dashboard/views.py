from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView

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

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})


class ListeningDeleteView(DeleteView):
    model = Listening
    success_url = reverse_lazy('main')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse(status=204, headers={'HX-Refresh': 'true'})
