from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='TestHome'),
    path('activities/', views.activity, name='qaAct'),
    path('activities/functional/',include('FuncTest.urls')),
    path('activities/UiAuto/',include('UiAuto.urls')),
    path('activities/ApiAuto/',include('ApiAuto.urls')),
]
