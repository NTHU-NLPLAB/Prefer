"""PREFER URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
# from index import get_index
import paraphrase.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('example/', paraphrase.views.get_example),
    path('index2/', paraphrase.views.get_paraphrase2),
    path('translate/', paraphrase.views.get_translation),
    path('wordlist/', paraphrase.views.get_wordlist),
    path('similar/', paraphrase.views.get_similar_paraphrase),
    path('extended/', paraphrase.views.get_extended_paraphrase),
    path('pattern/', paraphrase.views.get_pattern_paraphrase),
    path('preview/', paraphrase.views.preview),
    path('login/', paraphrase.views.login),
    path('validate/', paraphrase.views.validate_html),
    path('', paraphrase.views.get_paraphrase),
]
