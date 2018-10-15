from django.urls import path
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter
from API.views import *
from django.conf.urls import url
from .api import *

urlpatterns = [
    url(r'^login/', csrf_exempt(Login.as_view())),
     url(r'^createuser',UserManagement.as_view()),
     #url(r'^billings',Profilecheckout.as_view()),
     #url(r'^createtask',Createtask.as_view()),
     #url(r'^savegmail',Savegmail.as_view()),
     #url(r'^proxies',Proxies.as_view()),
     url(r'^shopify-url',ShopifyURL.as_view()),
 
]


router = SimpleRouter()
#router.register('login', UserViewSet)
router.register("billings", CheckoutViewSet)
router.register("createtask", TaskViewSet)
router.register("proxies", ProxiesViewSet)
router.register("savegmail", GmailAccountViewSet)



for url in router.urls:
    print(url)
    urlpatterns.append(url)


#urlpatterns.append(router.urls[0])


