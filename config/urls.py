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

urlpatterns = [
    path('admin/', admin.site.urls),

    (r'^PREFER/example.html', 'PREFER.PARAPHRASE.views.get_example' ),
    (r'^PREFER/index2.html', 'PREFER.PARAPHRASE.views.get_paraphrase2' ),
    (r'^PREFER/translate.html', 'PREFER.PARAPHRASE.views.get_translation' ),
    (r'^PREFER/wordlist.html', 'PREFER.PARAPHRASE.views.get_wordlist' ),
	(r'^PREFER/similar.html', 'PREFER.PARAPHRASE.views.get_similar_paraphrase' ),
	(r'^PREFER/extended.html', 'PREFER.PARAPHRASE.views.get_extended_paraphrase' ),
	(r'^PREFER/pattern.html', 'PREFER.PARAPHRASE.views.get_pattern_paraphrase' ),
	(r'^PREFER/preview.html', 'PREFER.PARAPHRASE.views.preview' ),
	(r'^PREFER/login.html', 'PREFER.PARAPHRASE.views.login' ),
	(r'^PREFER/validate.html', 'PREFER.PARAPHRASE.views.validate_html' ),
	(r'^PREFER/', 'PREFER.PARAPHRASE.views.get_paraphrase' ),
]
