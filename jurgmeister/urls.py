from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import homepage.views
import cocktails.views
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage.views.home, name='home'),
    path('services/',include('services.urls')),
    path('cocktails/',include('cocktails.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/login/pripol',homepage.views.pripol,name='pripol'),
    path('accounts/signup/pripol',homepage.views.pripol,name='pripol'),
    path('accounts/logout/pripol',homepage.views.pripol,name='pripol'),
    path('accounts/password/change/pripol',homepage.views.pripol,name='pripol'),
    path('accounts/password/set/pripol',homepage.views.pripol,name='pripol'),
    path('accounts/password/reset/pripol',homepage.views.pripol,name='pripol'),
    path('accounts/password/reset/done/pripol',homepage.views.pripol,name='pripol'),
    path('instagram/',homepage.views.instagram, name='instagram'),
    path('info/',homepage.views.info, name='info'),
    path('info/pripol/',homepage.views.pripolinfo, name='pripolinfo'),
    path('pripol/',homepage.views.pripol, name='pripol'),
    path('accounts/profile/', cocktails.views.your_account, name='account'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
