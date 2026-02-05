from django.urls import path

from dashboard.views import (ListeningListView, create_listening_popup,
                             ListeningCreateView)

urlpatterns = [
    path('', ListeningListView.as_view(), name='main'),
    path('modal-create/', create_listening_popup, name='popup_create'),
    path('create/', ListeningCreateView.as_view(), name='create_listening')
]
