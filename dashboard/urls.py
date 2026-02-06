from django.urls import path

from dashboard.views import (ListeningListView, create_listening_popup,
                             ListeningCreateView, ListeningDeleteView,
                             run_lemasson_parser_view)

urlpatterns = [
    path('', ListeningListView.as_view(), name='main'),
    path('modal-create/', create_listening_popup, name='popup_create'),
    path('create/', ListeningCreateView.as_view(), name='create_listening'),
    path('delete/<uuid:pk>/', ListeningDeleteView.as_view(),
         name='delete_listening'),
    path('parser-lemasson/', run_lemasson_parser_view,
         name='parser_lemasson')
]
