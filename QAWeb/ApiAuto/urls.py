from django.urls import path,include
from . import views


urlpatterns = [
   path('',views.index,name="apiAuto"),
   path('runapi/',views.runApiAutoTest,name="exeApi"),
   path('runapi/<int:sceId>',views.runApiAutoTest2,name="exeApi2"),
]
