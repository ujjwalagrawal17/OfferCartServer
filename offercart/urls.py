"""offercart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from about_us.views import about_us
from category.views import category
from city.views import city
from city.views import update_fcm
from contact_us.views import contact_us
from developers.views import developers
from myoffers.views import my_offers
from notification.views import send_notification, send_shops
from offer.views import send_offer, buy_offer, shop_offers, offer_add, offer_edit
from otp.views import send_otp
from otp.views import verify_otp
from payment.views import request_payment_hash, update_payment_status, wallet
from shop.views import shop, city_category, create_shop, verify_shop_otp, verify_shop_login, my_shop_profile, \
    edit_shop_profile
from splash_screen.views import splash_screen
from welcome.views import welcome

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^version/$', splash_screen),  # completed
    url(r'^send_otp/$', send_otp),
    url(r'^verify_otp/$', verify_otp),
    url(r'^wallet/$', wallet),
    url(r'^welcome/$', welcome),
    url(r'^city/$', city),
    url(r'^category/$', category),
    url(r'^shop/$', shop),
    url(r'^offer/$', send_offer),
    url(r'^my_offers/$', my_offers),
    url(r'^buy_offer/$', buy_offer),
    url(r'^about_us/$', about_us),
    url(r'^contact_us/$', contact_us),
    url(r'^developers/$', developers),
    url(r'^payment_hash/$', request_payment_hash),
    url(r'^update_payment_status/$', update_payment_status),
    url(r'^send_notification/$', send_notification),
    url(r'^send_shops/$', send_shops),
    url(r'^update_fcm/$', update_fcm),
    url(r'^city_category/$', city_category),
    url(r'^create_shop/$', create_shop),
    url(r'^verify_shop_otp/$', verify_shop_otp),
    url(r'^verify_shop_login/$', verify_shop_login),
    url(r'^my_shop_profile/$', my_shop_profile),
    url(r'^edit_shop_profile/$', edit_shop_profile),
    url(r'^shop_offers/$', shop_offers),
    url(r'^offer_add/$', offer_add),
    url(r'^offer_edit/$', offer_edit),


]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
