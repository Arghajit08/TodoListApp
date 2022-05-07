from django.urls import path
from .views import *

urlpatterns = [
    path('create', CreateView.as_view()),
    path('login', LoginView.as_view()),
    path('update', UpdateView.as_view()),
    path('delete', DeleteView.as_view()),
    
    
]