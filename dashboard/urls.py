from django.urls import path

from dashboard.views import ListeningListView

urlpatterns = [
    path('', ListeningListView.as_view(), name='main'),
]
