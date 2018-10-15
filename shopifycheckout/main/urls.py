from django.conf import settings
from django.conf.urls import url,static
from django.views.generic import TemplateView
from main import views

urlpattens = [
	url(r'^$',TemplateView.as_view(template_name='index.html'),name='home'),
	url(r'^api/crawl/',views.crawl,name='crawl'),
]

if settings.DEBUG:
	urlpattens += static.static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
	urlpattens += static.static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)