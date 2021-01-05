from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='funcIndex'),
    path('uploal_action/', views.upload_action, name='funcIndex'),
]

