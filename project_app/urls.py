# main urls.py 로부터 위임받은 urls
from django.urls import path
from project_app import views

urlpatterns = [
    path('insert',views.insertFunc), # 요쳥명이 같아도 get과 post방식으로 구분
    # path('insertok',views.insertokFunc),
    
     
    ]