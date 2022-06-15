"""FinalProject_one URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from project_app import views
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.mainFunc),
    path('show', views.findFunc),
    path('member/',include('project_app.urls')),
    # path('show/craw', views.craw_gmarket),
    path('basket', views.basketFunc), 
    path('show/reFinder', views.reFinderFunc),  # 장바구니에서 x 누르면 다시 상품 페이지로 이동.
    path('search', views.searchFunc),
    path('show/reset', views.resetFunc),
    path('show/show', views.findFunc),
    path('receipt', views.receipt),
    path('clear', views.clearFunc),
    #path('buy', views.buyFunc),
    
    
]
