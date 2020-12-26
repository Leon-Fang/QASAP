from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='TestHome'),
    path('activities/', views.activity, name='qaAct'),
]
